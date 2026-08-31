"""Data Models for Baofeng BF-F8HP Headless Programmer.

Defines strongly-typed dataclasses for memory channels, repeaters, geolocations,
NOAA weather stations, frequency plans, and subprocess execution results.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# CHIRP CSV Standard Header Schemas
CHIRP_CSV_HEADER_21: List[str] = [
    "Location",
    "Name",
    "Frequency",
    "Duplex",
    "Offset",
    "Tone",
    "rToneFreq",
    "cToneFreq",
    "DtcsCode",
    "DtcsPolarity",
    "RxDtcsCode",
    "CrossMode",
    "Mode",
    "TStep",
    "Skip",
    "Power",
    "Comment",
    "URCALL",
    "RPT1CALL",
    "RPT2CALL",
    "DVCODE",
]

CHIRP_CSV_HEADER_19: List[str] = [
    "Location",
    "Name",
    "Frequency",
    "Duplex",
    "Offset",
    "Tone",
    "rToneFreq",
    "cToneFreq",
    "DtcsCode",
    "DtcsPolarity",
    "Mode",
    "TStep",
    "Skip",
    "Power",
    "Comment",
    "URCALL",
    "RPT1CALL",
    "RPT2CALL",
    "DVCODE",
]

VALID_DUPLEX: Tuple[str, ...] = ("", "+", "-", "off", "split")
VALID_TONE: Tuple[str, ...] = ("", "Tone", "TSQL", "DTCS", "Cross")
VALID_MODE: Tuple[str, ...] = ("FM", "NFM", "Auto", "AM")
VALID_POWER: Tuple[str, ...] = ("High", "Med", "Low")
VALID_DTCS_POLARITY: Tuple[str, ...] = ("NN", "NR", "RN", "RR")
VALID_SKIP: Tuple[str, ...] = ("", "S")


@dataclass
class ChannelEntry:
    """Represents a single memory channel in the Baofeng / CHIRP memory map.

    Attributes:
        location: Channel slot index (0..127 for Baofeng BF-F8HP).
        name: Alphanumeric display name (max 7 characters for Baofeng LCD).
        frequency: Receive frequency in MHz (e.g. 146.520).
        duplex: Offset direction: '' (simplex), '+' (positive), '-' (negative),
                'off' (TX inhibit/RX only), 'split' (split frequency).
        offset: Frequency offset in MHz (e.g. 0.600000).
        tone: Tone mode: '' (none), 'Tone' (TX CTCSS), 'TSQL' (CTCSS squelch),
              'DTCS' (digital squelch), 'Cross' (cross tone).
        r_tone_freq: Repeater/TX CTCSS tone in Hz (default 88.5).
        c_tone_freq: Squelch/RX CTCSS tone in Hz (default 88.5).
        dtcs_code: 3-digit DCS code (default '023').
        dtcs_polarity: DCS polarity ('NN', 'NR', 'RN', 'RR').
        rx_dtcs_code: RX DCS code for split DCS (default '023').
        cross_mode: Cross mode tone relationship (default 'Tone->Tone').
        mode: Modulation mode ('FM' wide 25kHz, 'NFM' narrow 12.5kHz).
        tstep: Frequency tuning step in kHz (e.g. 2.5, 5.0, 6.25, 10.0, 12.5, 25.0).
        skip: Scan skip flag: '' (scanned), 'S' (skipped during scan).
        power: Transmit power level ('High' 8W, 'Med' 4W, 'Low' 1W).
        comment: Description or metadata for the channel.
        urcall: Digital voice URCALL (blank for analog Baofeng).
        rpt1call: Digital voice RPT1CALL (blank for analog Baofeng).
        rpt2call: Digital voice RPT2CALL (blank for analog Baofeng).
        dvcode: Digital voice code (blank for analog Baofeng).
    """

    location: int
    name: str
    frequency: float
    duplex: str = ""
    offset: float = 0.0
    tone: str = ""
    r_tone_freq: float = 88.5
    c_tone_freq: float = 88.5
    dtcs_code: str = "023"
    dtcs_polarity: str = "NN"
    rx_dtcs_code: str = "023"
    cross_mode: str = "Tone->Tone"
    mode: str = "FM"
    tstep: float = 5.0
    skip: str = ""
    power: str = "High"
    comment: str = ""
    urcall: str = ""
    rpt1call: str = ""
    rpt2call: str = ""
    dvcode: str = ""

    def __post_init__(self) -> None:
        """Sanitize and validate channel attributes on instantiation."""
        # Ensure location is an integer
        self.location = int(self.location)
        # Ensure frequency and offset are floats
        self.frequency = float(self.frequency)
        self.offset = float(self.offset)
        self.r_tone_freq = float(self.r_tone_freq)
        self.c_tone_freq = float(self.c_tone_freq)
        self.tstep = float(self.tstep)

        # Normalize string attributes
        self.name = self.sanitize_name(str(self.name))
        self.duplex = str(self.duplex).strip()
        self.tone = str(self.tone).strip()
        self.dtcs_code = str(self.dtcs_code).strip().zfill(3) if str(self.dtcs_code).strip() else "023"
        self.rx_dtcs_code = str(self.rx_dtcs_code).strip().zfill(3) if str(self.rx_dtcs_code).strip() else "023"
        self.dtcs_polarity = str(self.dtcs_polarity).strip().upper() or "NN"
        self.cross_mode = str(self.cross_mode).strip() or "Tone->Tone"
        self.mode = str(self.mode).strip().upper() or "FM"
        self.skip = str(self.skip).strip().upper()
        self.power = str(self.power).strip().capitalize() or "High"
        self.comment = str(self.comment).strip()
        self.urcall = str(self.urcall).strip()
        self.rpt1call = str(self.rpt1call).strip()
        self.rpt2call = str(self.rpt2call).strip()
        self.dvcode = str(self.dvcode).strip()

    @staticmethod
    def sanitize_name(raw_name: str, max_len: int = 7) -> str:
        """Sanitizes a channel name string for the Baofeng LCD display.

        Removes unsupported characters, converts to uppercase, and clips to max_len.
        Supported characters: A-Z, 0-9, hyphen, space, slash, plus.
        """
        if not raw_name:
            return ""
        # Remove characters outside standard alphanumeric and basic punctuation
        cleaned = re.sub(r"[^A-Za-z0-9\-\+\/\s\.]", "", str(raw_name))
        cleaned = cleaned.strip().upper()
        return cleaned[:max_len]

    def validate(self) -> List[str]:
        """Validates channel parameters against Baofeng BF-F8HP hardware limits.

        Returns:
            List of error description strings. Empty list indicates valid channel.
        """
        errors: List[str] = []

        if not (0 <= self.location <= 127):
            errors.append(f"Channel location {self.location} is out of bounds (0..127)")

        # VHF: 130.0 - 180.0 MHz, UHF: 400.0 - 521.0 MHz
        in_vhf = 130.0 <= self.frequency <= 180.0
        in_uhf = 400.0 <= self.frequency <= 521.0
        if not (in_vhf or in_uhf):
            errors.append(f"Frequency {self.frequency:.6f} MHz is outside Baofeng VHF/UHF bands (130-180 / 400-521 MHz)")

        if len(self.name) > 7:
            errors.append(f"Name '{self.name}' exceeds 7 characters maximum")

        if self.duplex not in VALID_DUPLEX:
            errors.append(f"Invalid duplex '{self.duplex}'. Must be one of {VALID_DUPLEX}")

        if self.tone not in VALID_TONE:
            errors.append(f"Invalid tone mode '{self.tone}'. Must be one of {VALID_TONE}")

        if self.mode not in VALID_MODE:
            errors.append(f"Invalid mode '{self.mode}'. Must be one of {VALID_MODE}")

        if self.power not in VALID_POWER:
            errors.append(f"Invalid power level '{self.power}'. Must be one of {VALID_POWER}")

        if self.dtcs_polarity not in VALID_DTCS_POLARITY:
            errors.append(f"Invalid DTCS polarity '{self.dtcs_polarity}'. Must be one of {VALID_DTCS_POLARITY}")

        if self.skip not in VALID_SKIP:
            errors.append(f"Invalid skip flag '{self.skip}'. Must be one of {VALID_SKIP}")

        return errors

    def to_dict(self, schema_19_col: bool = False) -> Dict[str, Any]:
        """Converts channel entry to a dictionary formatted for CHIRP CSV."""
        data: Dict[str, Any] = {
            "Location": self.location,
            "Name": self.name,
            "Frequency": f"{self.frequency:.6f}",
            "Duplex": self.duplex,
            "Offset": f"{self.offset:.6f}",
            "Tone": self.tone,
            "rToneFreq": f"{self.r_tone_freq:.1f}" if self.r_tone_freq else "88.5",
            "cToneFreq": f"{self.c_tone_freq:.1f}" if self.c_tone_freq else "88.5",
            "DtcsCode": self.dtcs_code,
            "DtcsPolarity": self.dtcs_polarity,
        }

        if not schema_19_col:
            data["RxDtcsCode"] = self.rx_dtcs_code
            data["CrossMode"] = self.cross_mode

        data.update(
            {
                "Mode": self.mode,
                "TStep": f"{self.tstep:.2f}",
                "Skip": self.skip,
                "Power": self.power,
                "Comment": self.comment,
                "URCALL": self.urcall,
                "RPT1CALL": self.rpt1call,
                "RPT2CALL": self.rpt2call,
                "DVCODE": self.dvcode,
            }
        )
        return data

    def to_csv_row(self, schema_19_col: bool = False) -> List[str]:
        """Converts channel entry to an ordered list of strings for CSV output."""
        headers = CHIRP_CSV_HEADER_19 if schema_19_col else CHIRP_CSV_HEADER_21
        d = self.to_dict(schema_19_col=schema_19_col)
        return [str(d.get(col, "")) for col in headers]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ChannelEntry:
        """Constructs a ChannelEntry instance from a dictionary (e.g. parsed CSV row)."""
        loc = int(d.get("Location", d.get("location", 0)))
        name = str(d.get("Name", d.get("name", "")))
        freq = float(d.get("Frequency", d.get("frequency", 0.0)))
        duplex = str(d.get("Duplex", d.get("duplex", "")))
        offset = float(d.get("Offset", d.get("offset", 0.0)) or 0.0)
        tone = str(d.get("Tone", d.get("tone", "")))
        r_tone = float(d.get("rToneFreq", d.get("r_tone_freq", 88.5)) or 88.5)
        c_tone = float(d.get("cToneFreq", d.get("c_tone_freq", 88.5)) or 88.5)
        dtcs = str(d.get("DtcsCode", d.get("dtcs_code", "023")))
        dtcs_pol = str(d.get("DtcsPolarity", d.get("dtcs_polarity", "NN")))
        rx_dtcs = str(d.get("RxDtcsCode", d.get("rx_dtcs_code", "023")))
        cross = str(d.get("CrossMode", d.get("cross_mode", "Tone->Tone")))
        mode = str(d.get("Mode", d.get("mode", "FM")))
        tstep = float(d.get("TStep", d.get("tstep", 5.0)) or 5.0)
        skip = str(d.get("Skip", d.get("skip", "")))
        power = str(d.get("Power", d.get("power", "High")))
        comment = str(d.get("Comment", d.get("comment", "")))
        urcall = str(d.get("URCALL", d.get("urcall", "")))
        rpt1call = str(d.get("RPT1CALL", d.get("rpt1call", "")))
        rpt2call = str(d.get("RPT2CALL", d.get("rpt2call", "")))
        dvcode = str(d.get("DVCODE", d.get("dvcode", "")))

        return cls(
            location=loc,
            name=name,
            frequency=freq,
            duplex=duplex,
            offset=offset,
            tone=tone,
            r_tone_freq=r_tone,
            c_tone_freq=c_tone,
            dtcs_code=dtcs,
            dtcs_polarity=dtcs_pol,
            rx_dtcs_code=rx_dtcs,
            cross_mode=cross,
            mode=mode,
            tstep=tstep,
            skip=skip,
            power=power,
            comment=comment,
            urcall=urcall,
            rpt1call=rpt1call,
            rpt2call=rpt2call,
            dvcode=dvcode,
        )


@dataclass
class RepeaterInfo:
    """Represents raw amateur radio repeater metadata sourced from RepeaterBook or offline cache.

    Attributes:
        callsign: Repeater trustee/club callsign (e.g. 'K4GAS', 'W4P').
        frequency: Output/downlink frequency in MHz (e.g. 146.940).
        offset: Transmit shift in MHz (e.g. 0.600 or 5.000).
        duplex: Offset direction ('+', '-', or '').
        tone_mode: Tone mode string ('Tone', 'TSQL', 'DTCS', or '').
        tone_freq: CTCSS access tone in Hz (e.g. 123.0).
        dcs_code: DCS digital code (e.g. '023').
        city: City or nearest municipality.
        state: US state name or 2-letter abbreviation.
        distance_miles: Distance from query center coordinates in miles.
        on_air: True if status is operational / On-Air.
        ares: True if flagged for ARES emergency communications.
        races: True if flagged for RACES emergency communications.
        skywarn: True if designated for SKYWARN severe weather nets.
        linked: True if part of a linked wide-area repeater network.
        county: County name.
        latitude: Station latitude in degrees.
        longitude: Station longitude in degrees.
        use: Access policy ('OPEN', 'CLOSED', 'PRIVATE').
        operational_status: Verbatim operational status string (e.g. 'On-Air', 'Off-Air').
    """

    callsign: str
    frequency: float
    offset: float = 0.0
    duplex: str = ""
    tone_mode: str = ""
    tone_freq: float = 88.5
    dcs_code: str = ""
    city: str = ""
    state: str = ""
    distance_miles: float = 0.0
    on_air: bool = True
    ares: bool = False
    races: bool = False
    skywarn: bool = False
    linked: bool = False
    county: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    use: str = "OPEN"
    operational_status: str = "On-Air"
    comment: str = ""
    mode: str = "FM"

    def is_emergency_or_linked(self) -> bool:
        """Returns True if the repeater is designated for emergency communications or linked nets."""
        return self.ares or self.races or self.skywarn or self.linked

    def priority_score(self) -> float:
        """Computes a priority sorting score for memory allocation.

        Higher score = higher priority.
        On-Air repeaters with emergency/linked designations rank highest,
        weighted inversely by distance.
        """
        if not self.on_air:
            return -1000.0

        score = 100.0
        if self.ares:
            score += 40.0
        if self.skywarn:
            score += 40.0
        if self.races:
            score += 30.0
        if self.linked:
            score += 35.0

        # Distance penalty: closer repeaters get higher score
        score -= min(self.distance_miles, 100.0) * 0.5
        return score

    def to_channel_entry(self, location: int, power: str = "High") -> ChannelEntry:
        """Converts this repeater into a standardized ChannelEntry."""
        # Generate clean display name (max 7 chars): e.g. callsign or city+band
        display_name = self.callsign.strip().replace("-", "")
        if not display_name or len(display_name) > 7:
            # Fallback to city or freq tag
            tag = self.city.strip().upper().replace(" ", "")[:4]
            band = "2M" if self.frequency < 200.0 else "70"
            display_name = f"{tag}{band}"[:7]

        # Determine tone mode
        t_mode = self.tone_mode
        if not t_mode and self.tone_freq > 0:
            t_mode = "Tone"

        comment_parts = [self.callsign, self.city, self.state]
        if self.ares:
            comment_parts.append("ARES")
        if self.skywarn:
            comment_parts.append("SKYWARN")
        if self.linked:
            comment_parts.append("LINKED")
        comment = " - ".join(filter(None, comment_parts))

        return ChannelEntry(
            location=location,
            name=ChannelEntry.sanitize_name(display_name, max_len=7),
            frequency=self.frequency,
            duplex=self.duplex,
            offset=self.offset,
            tone=t_mode,
            r_tone_freq=self.tone_freq if self.tone_freq > 0 else 88.5,
            c_tone_freq=self.tone_freq if self.tone_freq > 0 else 88.5,
            dtcs_code=self.dcs_code or "023",
            power=power,
            mode="FM",
            comment=comment,
        )


@dataclass
class GeoLocation:
    """Represents resolved geographical information for a US Zip Code.

    Attributes:
        zip_code: 5-digit US Postal Code.
        city: Primary municipality name.
        state: Full state name or state abbreviation.
        latitude: Geographic latitude in decimal degrees.
        longitude: Geographic longitude in decimal degrees.
        fips_state: 2-digit US FIPS State Code (e.g. '13' for Georgia).
        county: County or administrative parish name.
        state_abbreviation: 2-letter state postal abbreviation (e.g. 'GA').
    """

    zip_code: str
    city: str
    state: str
    latitude: float
    longitude: float
    fips_state: str = ""
    county: str = ""
    state_abbreviation: str = ""

    @property
    def state_abbr(self) -> str:
        """Returns the 2-letter state abbreviation."""
        return self.state_abbreviation or (self.state if len(self.state) == 2 else "")


@dataclass
class NOAAStation:
    """Represents a standard NOAA All-Hazards Weather Radio VHF frequency.

    Attributes:
        channel_num: WX channel index (1..7).
        frequency: Receive frequency in MHz (e.g. 162.550).
        name: Alphanumeric display name (e.g. 'WX1-55').
        description: Description of the channel and frequency.
    """

    channel_num: int
    frequency: float
    name: str
    description: str = ""

    def to_channel_entry(self, location: int, power: str = "Low") -> ChannelEntry:
        """Converts NOAA station to a safe, RX-only ChannelEntry with TX inhibit."""
        return ChannelEntry(
            location=location,
            name=self.name,
            frequency=self.frequency,
            duplex="off",  # TX Inhibit for receive-only safety
            offset=0.0,
            tone="",
            mode="FM",
            power=power,
            skip="",
            comment=self.description or f"NOAA Weather Radio {self.name} ({self.frequency:.3f} MHz)",
        )


@dataclass
class SubprocessResult:
    """Represents the execution result of a CLI subprocess (e.g. chirpc).

    Attributes:
        returncode: Process exit code (0 for success).
        stdout: Captured standard output string.
        stderr: Captured standard error string.
        command: Command-line list or string executed.
        duration_seconds: Elapsed execution duration in seconds.
    """

    returncode: int
    stdout: str
    stderr: str
    command: Any
    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        """Returns True if the subprocess exited cleanly with returncode 0."""
        return self.returncode == 0


@dataclass
class RadioProfile:
    """Hardware capability profile and operational boundaries for a radio transceiver.

    Defaults configured for the Baofeng BF-F8HP.
    """

    vendor: str = "Baofeng"
    model: str = "BF-F8HP"
    chirp_model_id: str = "Baofeng_BF-F8HP"
    max_channels: int = 128
    channel_bounds: Tuple[int, int] = (0, 127)
    power_levels: Tuple[str, ...] = ("High", "Med", "Low")
    name_max_len: int = 7
    vhf_range: Tuple[float, float] = (130.0, 180.0)
    uhf_range: Tuple[float, float] = (400.0, 521.0)
    eeprom_size: int = 0x1808  # 6152 bytes
    baud_rate: int = 9600


@dataclass
class FrequencyPlan:
    """Complete synthesized frequency programming plan for a radio.

    Attributes:
        zip_code: Target US Zip Code.
        geo_location: Resolved geographical location metadata.
        channels: List of all allocated ChannelEntry objects (0..127).
        repeaters_count: Count of amateur repeaters in plan.
        noaa_count: Count of NOAA weather channels in plan.
        gmrs_count: Count of GMRS/FRS channels in plan.
        simplex_count: Count of national calling simplex channels in plan.
    """

    zip_code: str
    geo_location: Optional[GeoLocation] = None
    channels: List[ChannelEntry] = field(default_factory=list)
    repeaters_count: int = 0
    noaa_count: int = 0
    gmrs_count: int = 0
    simplex_count: int = 0

    @property
    def total_channels(self) -> int:
        """Returns total number of programmed memory channels."""
        return len(self.channels)
