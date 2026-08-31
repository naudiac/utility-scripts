"""Dynamic Frequency Sourcing and Synthesis Module for Baofeng BF-F8HP.

Provides automated geocoding, RepeaterBook querying, NOAA weather radio integration,
GMRS/FRS channel synthesis, National Calling channel injection, and priority sorting.
"""

from __future__ import annotations

import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from .models import ChannelEntry, FrequencyPlan, GeoLocation, NOAAStation, RepeaterInfo
    from .offline_data import (
        GMRS_FRS_CHANNELS,
        NATIONAL_SIMPLEX_CALLING,
        NOAA_WEATHER_STATIONS,
        OFFLINE_REPEATERS,
        OFFLINE_ZIP_GEO,
        STANDARD_CTCSS_TONES,
        US_STATE_TO_FIPS,
    )
except (ImportError, ValueError):
    from models import ChannelEntry, FrequencyPlan, GeoLocation, NOAAStation, RepeaterInfo
    from offline_data import (
        GMRS_FRS_CHANNELS,
        NATIONAL_SIMPLEX_CALLING,
        NOAA_WEATHER_STATIONS,
        OFFLINE_REPEATERS,
        OFFLINE_ZIP_GEO,
        STANDARD_CTCSS_TONES,
        US_STATE_TO_FIPS,
    )


class FrequencyFetcher:
    """Sourcing client for geocoding, amateur radio repeaters, NOAA, and GMRS channels."""

    DEFAULT_USER_AGENT = "BaofengProgrammer/1.0 (+https://github.com/naudiac/baofeng-headless-programmer; radio@example.com)"
    ZIPPOPOTAM_URL_TEMPLATE = "https://api.zippopotam.us/us/{zip_code}"
    REPEATERBOOK_EXPORT_URL = "https://www.repeaterbook.com/api/export.php"

    def __init__(
        self,
        user_agent: Optional[str] = None,
        timeout: float = 5.0,
        repeaterbook_token: Optional[str] = None,
    ) -> None:
        """Initializes the frequency fetcher with network configuration and authentication."""
        self.user_agent = user_agent or self.DEFAULT_USER_AGENT
        self.timeout = timeout
        self.token = repeaterbook_token

    def build_request_headers(self) -> Dict[str, str]:
        """Constructs compliant HTTP request headers for external API queries."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }
        if self.token:
            headers["X-RB-App-Token"] = self.token
        return headers

    def is_valid_zip_code(self, zip_code: str) -> bool:
        """Validates whether a string is a standard 5-digit US postal code."""
        if not isinstance(zip_code, str):
            return False
        return bool(re.match(r"^\d{5}$", zip_code.strip()))

    def is_valid_radius(self, radius_miles: float) -> bool:
        """Validates whether the search radius is within acceptable bounds (1 to 100 miles)."""
        if not isinstance(radius_miles, (int, float)):
            return False
        return 0.0 < float(radius_miles) <= 100.0

    def is_valid_ctcss_tone(self, tone: float) -> bool:
        """Validates whether a CTCSS sub-audible tone is within standard EIA boundaries."""
        if not isinstance(tone, (int, float)):
            return False
        tone_float = float(tone)
        if not (67.0 <= tone_float <= 254.1):
            return False
        # Match standard 50 EIA tones with small float tolerance
        return any(abs(tone_float - t) < 0.15 for t in STANDARD_CTCSS_TONES)

    def get_fips_code(self, state_abbr: str) -> Optional[str]:
        """Translates a US State 2-letter postal abbreviation into its 2-digit FIPS code."""
        if not state_abbr:
            return None
        return US_STATE_TO_FIPS.get(str(state_abbr).strip().upper())

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates great-circle distance between two geodetic coordinates using Haversine formula."""
        if (lat1 == lat2) and (lon1 == lon2):
            return 0.0

        earth_radius_miles = 3958.8
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return earth_radius_miles * c

    def resolve_zip(self, zip_code: str, mock: bool = False) -> GeoLocation:
        """Resolves a 5-digit US Postal Code to geographic coordinates and state metadata."""
        clean_zip = str(zip_code).strip()

        # Check offline cache first if in mock mode
        if mock:
            if clean_zip in OFFLINE_ZIP_GEO:
                cached = OFFLINE_ZIP_GEO[clean_zip]
                return GeoLocation(
                    zip_code=clean_zip,
                    city=cached["city"],
                    state=cached["state"],
                    latitude=float(cached["latitude"]),
                    longitude=float(cached["longitude"]),
                    fips_state=cached.get("fips_state", ""),
                    county=cached.get("county", ""),
                    state_abbreviation=cached.get("state_abbr", ""),
                )
            # Default fallback for mock mode if zip code not in offline table
            return GeoLocation(
                zip_code=clean_zip,
                city="Metter",
                state="Georgia",
                latitude=32.397,
                longitude=-81.979,
                fips_state="13",
                county="Candler",
                state_abbreviation="GA",
            )

        # Attempt live geocoding query
        try:
            url = self.ZIPPOPOTAM_URL_TEMPLATE.format(zip_code=clean_zip)
            req = urllib.request.Request(url, headers=self.build_request_headers())
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    places = payload.get("places", [])
                    if places:
                        primary_place = places[0]
                        city = primary_place.get("place name", "")
                        state = primary_place.get("state", "")
                        state_abbr = primary_place.get("state abbreviation", "")
                        lat = float(primary_place.get("latitude", 0.0))
                        lon = float(primary_place.get("longitude", 0.0))
                        fips = self.get_fips_code(state_abbr) or ""
                        return GeoLocation(
                            zip_code=clean_zip,
                            city=city,
                            state=state,
                            latitude=lat,
                            longitude=lon,
                            fips_state=fips,
                            county=primary_place.get("county", ""),
                            state_abbreviation=state_abbr,
                        )
        except Exception:
            pass

        # Offline fallback upon network or HTTP failure
        if clean_zip in OFFLINE_ZIP_GEO:
            cached = OFFLINE_ZIP_GEO[clean_zip]
            return GeoLocation(
                zip_code=clean_zip,
                city=cached["city"],
                state=cached["state"],
                latitude=float(cached["latitude"]),
                longitude=float(cached["longitude"]),
                fips_state=cached.get("fips_state", ""),
                county=cached.get("county", ""),
                state_abbreviation=cached.get("state_abbr", ""),
            )

        # Final fallback return
        return GeoLocation(
            zip_code=clean_zip,
            city="Metter",
            state="Georgia",
            latitude=32.397,
            longitude=-81.979,
            fips_state="13",
            county="Candler",
            state_abbreviation="GA",
        )

    def parse_repeaterbook_response(
        self,
        raw_items: List[Dict[str, Any]],
        origin_lat: Optional[float] = None,
        origin_lon: Optional[float] = None,
    ) -> List[RepeaterInfo]:
        """Parses raw RepeaterBook export JSON dictionaries into strongly-typed RepeaterInfo models."""
        repeaters: List[RepeaterInfo] = []

        for item in raw_items:
            callsign = str(item.get("Callsign", item.get("callsign", ""))).strip()
            freq_str = str(item.get("Frequency", item.get("frequency", "0"))).strip()
            try:
                frequency = float(freq_str)
            except ValueError:
                continue

            if frequency <= 0.0:
                continue

            # Calculate frequency offset and duplex direction
            input_freq_str = str(item.get("Input Freq", item.get("input_freq", ""))).strip()
            offset = 0.0
            duplex = ""

            if input_freq_str:
                try:
                    in_freq = float(input_freq_str)
                    shift = in_freq - frequency
                    if abs(shift) > 0.0001:
                        offset = round(abs(shift), 4)
                        duplex = "+" if shift > 0 else "-"
                except ValueError:
                    pass

            if not duplex:
                offset_val = item.get("Offset", item.get("offset", 0.0))
                try:
                    offset = float(offset_val) if offset_val else 0.0
                except (ValueError, TypeError):
                    offset = 0.0
                duplex = str(item.get("Duplex", item.get("duplex", ""))).strip()
                if not duplex and offset > 0.0:
                    duplex = "-" if frequency < 200.0 else "+"

            # Tone handling (CTCSS PL / TSQ / DCS)
            pl_str = str(item.get("PL", item.get("tone_freq", item.get("rToneFreq", "")))).strip()
            tsq_str = str(item.get("TSQ", item.get("cToneFreq", ""))).strip()
            tone_mode = str(item.get("tone_mode", item.get("Tone", ""))).strip()
            tone_freq = 88.5

            if pl_str:
                try:
                    tone_freq = float(pl_str)
                except ValueError:
                    tone_freq = 88.5

            if not tone_mode:
                if tsq_str:
                    try:
                        if float(tsq_str) > 0:
                            tone_mode = "TSQL"
                            tone_freq = float(tsq_str)
                    except ValueError:
                        pass
                if not tone_mode and pl_str:
                    try:
                        if float(pl_str) > 0:
                            tone_mode = "Tone"
                    except ValueError:
                        pass

            dcs_code = str(item.get("DCS", item.get("dcs_code", item.get("DtcsCode", "023")))).strip().zfill(3)

            city = str(item.get("Nearest City", item.get("city", ""))).strip()
            state = str(item.get("State", item.get("state", ""))).strip()
            county = str(item.get("County", item.get("county", ""))).strip()

            # Operational Status parsing
            op_status = str(item.get("Operational Status", item.get("operational_status", ""))).strip()
            op_lower = op_status.lower()
            if op_lower:
                is_off = "off" in op_lower or "test" in op_lower or "decomm" in op_lower or "inactive" in op_lower
                on_air = ("on" in op_lower or "operat" in op_lower) and not is_off
            else:
                on_air = bool(item.get("on_air", True))

            # Emergency communication & linked network flags
            def parse_bool_flag(key: str, default: bool = False) -> bool:
                val = item.get(key, item.get(key.lower(), default))
                if isinstance(val, bool):
                    return val
                return str(val).strip().lower() in ("yes", "true", "1", "y")

            ares = parse_bool_flag("ARES")
            races = parse_bool_flag("RACES")
            skywarn = parse_bool_flag("SKYWARN")
            linked = parse_bool_flag("Linked") or parse_bool_flag("linked")

            # Coordinates and distance calculation
            lat = float(item.get("Latitude", item.get("latitude", 0.0)) or 0.0)
            lon = float(item.get("Longitude", item.get("longitude", 0.0)) or 0.0)
            distance_miles = float(item.get("distance_miles", item.get("distance", 0.0)) or 0.0)

            if origin_lat is not None and origin_lon is not None and lat != 0.0 and lon != 0.0:
                distance_miles = round(self.calculate_distance(origin_lat, origin_lon, lat, lon), 1)

            use = str(item.get("Use", item.get("use", "OPEN"))).strip()

            repeaters.append(
                RepeaterInfo(
                    callsign=callsign or "RPT",
                    frequency=frequency,
                    offset=offset,
                    duplex=duplex,
                    tone_mode=tone_mode,
                    tone_freq=tone_freq,
                    dcs_code=dcs_code,
                    city=city,
                    state=state,
                    distance_miles=distance_miles,
                    on_air=on_air,
                    ares=ares,
                    races=races,
                    skywarn=skywarn,
                    linked=linked,
                    county=county,
                    latitude=lat,
                    longitude=lon,
                    use=use,
                    operational_status=op_status or ("On-air" if on_air else "Off-air"),
                )
            )

        return repeaters

    def fetch_repeaters(
        self,
        zip_code: str,
        radius_miles: float = 35.0,
        max_count: int = 90,
        mock: bool = False,
        token: Optional[str] = None,
    ) -> List[RepeaterInfo]:
        """Queries RepeaterBook API for active repeaters within radius; falls back to offline cache."""
        clean_zip = str(zip_code).strip()
        geo = self.resolve_zip(clean_zip, mock=mock)
        active_token = token or self.token

        repeaters: List[RepeaterInfo] = []

        # If live and authenticated, attempt network API query
        if not mock and active_token and geo.fips_state:
            try:
                params = {
                    "state_id": geo.fips_state,
                    "mode": "analog",
                }
                url = f"{self.REPEATERBOOK_EXPORT_URL}?{urllib.parse.urlencode(params)}"
                req = urllib.request.Request(url, headers=self.build_request_headers())
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        payload = json.loads(resp.read().decode("utf-8"))
                        if isinstance(payload, list):
                            repeaters = self.parse_repeaterbook_response(
                                payload, origin_lat=geo.latitude, origin_lon=geo.longitude
                            )
            except Exception:
                pass

        # If no repeaters obtained or in mock mode, load from offline database
        if not repeaters:
            raw_offline = OFFLINE_REPEATERS.get(clean_zip, OFFLINE_REPEATERS.get("30445", []))
            repeaters = self.parse_repeaterbook_response(
                raw_offline, origin_lat=geo.latitude, origin_lon=geo.longitude
            )

        # Apply filtering & prioritization pipeline
        filtered_on_air = self.filter_on_air(repeaters)
        filtered_radius = self.filter_by_radius(filtered_on_air, max_radius_miles=radius_miles)
        prioritized = self.prioritize_repeaters(filtered_radius)

        return prioritized[:max_count]

    def filter_by_radius(
        self, repeaters: List[RepeaterInfo], max_radius_miles: float = 35.0
    ) -> List[RepeaterInfo]:
        """Filters a list of repeaters strictly to those within the given radius."""
        return [r for r in repeaters if r.distance_miles <= max_radius_miles]

    def filter_on_air(self, repeaters: List[RepeaterInfo]) -> List[RepeaterInfo]:
        """Strictly filters repeaters to those with operational 'On-Air' status."""
        return [r for r in repeaters if r.on_air]

    def prioritize_repeaters(self, repeaters: List[RepeaterInfo]) -> List[RepeaterInfo]:
        """Sorts repeaters by priority score (ARES/SKYWARN/Linked emergency repeaters first, then distance)."""
        return sorted(repeaters, key=lambda r: r.priority_score(), reverse=True)

    def filter_by_bands(self, repeaters: List[RepeaterInfo], bands: List[str]) -> List[RepeaterInfo]:
        """Filters repeaters based on amateur frequency bands (e.g. '2m', '70cm', 'all')."""
        if not bands or "all" in [b.lower() for b in bands]:
            return list(repeaters)

        normalized_bands = {b.lower().strip() for b in bands}
        results: List[RepeaterInfo] = []

        for r in repeaters:
            in_2m = 144.0 <= r.frequency <= 148.0
            in_70cm = 420.0 <= r.frequency <= 450.0

            if "2m" in normalized_bands and in_2m:
                results.append(r)
            elif "70cm" in normalized_bands and in_70cm:
                results.append(r)

        return results

    def get_noaa_channels(self, power: str = "Low") -> List[ChannelEntry]:
        """Generates the standard 7 NOAA All-Hazards Weather Radio channels with TX inhibit."""
        channels: List[ChannelEntry] = []
        for idx, station in enumerate(NOAA_WEATHER_STATIONS):
            channels.append(
                ChannelEntry(
                    location=idx,
                    name=station["name"],
                    frequency=float(station["frequency"]),
                    duplex="off",
                    offset=0.0,
                    tone="",
                    mode="FM",
                    power=power,
                    skip="",
                    comment=station["description"],
                )
            )
        return channels

    def get_simplex_calling(self, power: str = "High") -> ChannelEntry:
        """Generates the standard National 2m VHF Simplex Calling Channel (146.520 MHz)."""
        info = NATIONAL_SIMPLEX_CALLING["2m"]
        return ChannelEntry(
            location=0,
            name=info["name"],
            frequency=float(info["frequency"]),
            duplex="",
            offset=0.0,
            tone="",
            mode="FM",
            tstep=float(info.get("tstep", 5.0)),
            power=power,
            comment=info["comment"],
        )

    def get_gmrs_frs_channels(self, power: str = "High") -> List[ChannelEntry]:
        """Generates standard GMRS / FRS Channels 1-22 simplex memory entries."""
        channels: List[ChannelEntry] = []
        for idx, ch_info in enumerate(GMRS_FRS_CHANNELS):
            channels.append(
                ChannelEntry(
                    location=idx,
                    name=ch_info["name"],
                    frequency=float(ch_info["frequency"]),
                    duplex="",
                    offset=0.0,
                    tone="",
                    mode="FM",
                    tstep=5.0,
                    power=power,
                    comment=ch_info["comment"],
                )
            )
        return channels

    def build_frequency_plan_from_components(
        self,
        repeaters: List[RepeaterInfo],
        include_noaa: bool = True,
        include_gmrs: bool = True,
        include_calling: bool = True,
        repeater_start_channel: int = 1,
        noaa_start_channel: Optional[int] = None,
        max_total_channels: int = 128,
        power: str = "High",
    ) -> List[ChannelEntry]:
        """Synthesizes a unified, collision-free frequency plan within the 128-channel capacity limit."""
        allocated_slots: Dict[int, ChannelEntry] = {}
        reserved_slots: Set[int] = set()

        # 1. Determine reserved slots for NOAA if explicit starting index given
        noaa_channels = self.get_noaa_channels(power="Low") if include_noaa else []
        if include_noaa and noaa_start_channel is not None:
            for idx in range(len(noaa_channels)):
                slot = noaa_start_channel + idx
                if slot < max_total_channels:
                    reserved_slots.add(slot)

        # 2. Allocate National VHF Simplex Calling Channel (Channel 0 by default)
        if include_calling:
            calling_ch = self.get_simplex_calling(power=power)
            slot = 0
            if slot in reserved_slots or slot >= max_total_channels:
                slot = next((s for s in range(max_total_channels) if s not in reserved_slots and s not in allocated_slots), 0)
            calling_ch.location = slot
            allocated_slots[slot] = calling_ch

        # 3. Calculate memory quotas for repeaters
        fixed_count = len(allocated_slots) + (len(noaa_channels) if include_noaa else 0)
        gmrs_needed = 22 if include_gmrs else 0
        max_repeaters_allowed = max(0, max_total_channels - fixed_count - gmrs_needed)

        # 4. Allocate Prioritized Repeaters
        on_air_repeaters = self.filter_on_air(repeaters)
        prioritized_repeaters = self.prioritize_repeaters(on_air_repeaters)

        current_rep_slot = repeater_start_channel
        reps_added = 0
        for rep in prioritized_repeaters:
            if reps_added >= max_repeaters_allowed:
                break
            # Find next free slot not in reserved or allocated
            while current_rep_slot < max_total_channels and (
                current_rep_slot in allocated_slots or current_rep_slot in reserved_slots
            ):
                current_rep_slot += 1

            if current_rep_slot >= max_total_channels:
                break

            entry = rep.to_channel_entry(location=current_rep_slot, power=power)
            allocated_slots[current_rep_slot] = entry
            reps_added += 1
            current_rep_slot += 1

        # 5. Allocate GMRS / FRS Channels (1-22)
        if include_gmrs:
            gmrs_list = self.get_gmrs_frs_channels(power=power)
            current_gmrs_slot = current_rep_slot
            for g_ch in gmrs_list:
                if len(allocated_slots) + (len(noaa_channels) if include_noaa and noaa_start_channel is None else 0) >= max_total_channels:
                    break
                while current_gmrs_slot < max_total_channels and (
                    current_gmrs_slot in allocated_slots or current_gmrs_slot in reserved_slots
                ):
                    current_gmrs_slot += 1

                if current_gmrs_slot >= max_total_channels:
                    break

                g_ch.location = current_gmrs_slot
                allocated_slots[current_gmrs_slot] = g_ch
                current_gmrs_slot += 1

        # 6. Allocate NOAA Weather Radio Channels
        if include_noaa:
            if noaa_start_channel is not None:
                for idx, n_ch in enumerate(noaa_channels):
                    target_slot = noaa_start_channel + idx
                    if target_slot < max_total_channels:
                        n_ch.location = target_slot
                        allocated_slots[target_slot] = n_ch
            else:
                # Place NOAA channels in remaining available slots
                current_noaa_slot = current_gmrs_slot if include_gmrs else current_rep_slot
                for n_ch in noaa_channels:
                    if len(allocated_slots) >= max_total_channels:
                        break
                    while current_noaa_slot < max_total_channels and current_noaa_slot in allocated_slots:
                        current_noaa_slot += 1
                    if current_noaa_slot >= max_total_channels:
                        break
                    n_ch.location = current_noaa_slot
                    allocated_slots[current_noaa_slot] = n_ch
                    current_noaa_slot += 1

        # Return ordered channel list
        result = [allocated_slots[slot] for slot in sorted(allocated_slots.keys())]
        return result[:max_total_channels]

    def build_frequency_plan(
        self,
        zip_code: str,
        max_total_channels: int = 128,
        mock: bool = False,
        repeater_start_channel: int = 1,
        noaa_start_channel: Optional[int] = None,
        power: str = "High",
        bands: Optional[List[str]] = None,
        radius_miles: float = 35.0,
    ) -> List[ChannelEntry]:
        """Builds a complete, prioritized frequency plan for a target US Postal Code."""
        repeaters = self.fetch_repeaters(
            zip_code=zip_code,
            radius_miles=radius_miles,
            max_count=90,
            mock=mock,
        )

        if bands:
            repeaters = self.filter_by_bands(repeaters, bands)

        return self.build_frequency_plan_from_components(
            repeaters=repeaters,
            include_noaa=True,
            include_gmrs=True,
            include_calling=True,
            repeater_start_channel=repeater_start_channel,
            noaa_start_channel=noaa_start_channel,
            max_total_channels=max_total_channels,
            power=power,
        )
