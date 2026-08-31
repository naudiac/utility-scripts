"""CHIRP CSV Engine for Baofeng BF-F8HP Headless Programmer.

Handles 19-column and 21-column CHIRP CSV serialization, deserialization,
channel memory allocation, de-duplication, collision avoidance, and LCD tag sanitization.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from .models import (
        CHIRP_CSV_HEADER_19,
        CHIRP_CSV_HEADER_21,
        VALID_DUPLEX,
        VALID_MODE,
        VALID_POWER,
        VALID_TONE,
        ChannelEntry,
    )
except (ImportError, ValueError):
    from models import (
        CHIRP_CSV_HEADER_19,
        CHIRP_CSV_HEADER_21,
        VALID_DUPLEX,
        VALID_MODE,
        VALID_POWER,
        VALID_TONE,
        ChannelEntry,
    )


class CSVEngine:
    """Serialization, deserialization, and channel management engine for CHIRP CSV files."""

    VHF_MIN_FREQ = 136.000000
    VHF_MAX_FREQ = 174.000000
    UHF_MIN_FREQ = 400.000000
    UHF_MAX_FREQ = 520.000000

    def __init__(self, default_schema_19_col: bool = True) -> None:
        """Initializes the CSV engine with default schema settings."""
        self.default_schema_19_col = default_schema_19_col

    def sanitize_channel_name(self, name: str, max_len: int = 7) -> str:
        """Sanitizes a channel name string for the Baofeng LCD display.

        Removes unsupported characters (slashes, symbols, punctuation),
        converts to uppercase, and clips to max_len (default 7 chars).
        Supported characters: A-Z, 0-9, hyphen (-), space ( ).
        """
        if not name:
            return ""
        # Strip all characters except alphanumeric, hyphen, and space
        cleaned = re.sub(r"[^A-Za-z0-9\-\s]", "", str(name))
        cleaned = cleaned.strip().upper()
        return cleaned[:max_len]

    def is_valid_channel_location(self, location: int) -> bool:
        """Validates if a channel location index is within the Baofeng BF-F8HP memory bank (0..127)."""
        if not isinstance(location, int):
            return False
        return 0 <= location <= 127

    def is_valid_frequency(self, frequency: float) -> bool:
        """Validates if a frequency is within the Baofeng VHF (136-174 MHz) or UHF (400-520 MHz) bands."""
        if not isinstance(frequency, (int, float)):
            return False
        freq_val = float(frequency)
        in_vhf = self.VHF_MIN_FREQ <= freq_val <= self.VHF_MAX_FREQ
        in_uhf = self.UHF_MIN_FREQ <= freq_val <= self.UHF_MAX_FREQ
        return in_vhf or in_uhf

    def format_dtcs_code(self, code: Any) -> str:
        """Formats a DCS digital code as a 3-digit zero-padded string."""
        if not code:
            return "023"
        digits = re.sub(r"\D", "", str(code))
        if not digits:
            return "023"
        return digits.zfill(3)

    def is_valid_offset(self, offset: float) -> bool:
        """Validates if a repeater offset is within acceptable bounds (0.0 to 70.0 MHz)."""
        if not isinstance(offset, (int, float)):
            return False
        return 0.0 <= float(offset) <= 70.0

    def export_csv(
        self,
        channels: List[ChannelEntry],
        output_path: Path,
        schema_19_col: Optional[bool] = None,
    ) -> Path:
        """Serializes a list of ChannelEntry objects to a strictly-compliant CHIRP CSV file.

        Args:
            channels: List of ChannelEntry objects to serialize.
            output_path: Target filesystem path for the output CSV file.
            schema_19_col: If True, writes standard 19-column schema; if False, writes 21-column schema.

        Returns:
            Resolved Path of the written CSV file.
        """
        use_19_col = self.default_schema_19_col if schema_19_col is None else schema_19_col
        headers = CHIRP_CSV_HEADER_19 if use_19_col else CHIRP_CSV_HEADER_21

        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for channel in channels:
                row = channel.to_csv_row(schema_19_col=use_19_col)
                writer.writerow(row)

        return path

    def import_csv(self, input_path: Path) -> List[ChannelEntry]:
        """Parses a CHIRP CSV file into a list of strongly-typed ChannelEntry objects.

        Args:
            input_path: Path to the input CSV file.

        Returns:
            List of parsed ChannelEntry objects.
        """
        path = Path(input_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")

        channels: List[ChannelEntry] = []

        with open(path, mode="r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header_row = next(reader, None)
            if not header_row:
                return []

            headers = [h.strip() for h in header_row]

            for row in reader:
                if not row or not any(row):
                    continue

                # Build dictionary mapping column name to value
                row_dict: Dict[str, Any] = {}
                for idx, col_name in enumerate(headers):
                    if idx < len(row):
                        row_dict[col_name] = row[idx].strip()

                if "Location" not in row_dict and "location" not in row_dict:
                    # Fallback to positional mapping if location header missing
                    try:
                        row_dict["Location"] = int(row[0])
                    except (ValueError, IndexError):
                        continue

                try:
                    entry = ChannelEntry.from_dict(row_dict)
                    channels.append(entry)
                except Exception:
                    continue

        return channels

    def merge_channels(
        self,
        existing_channels: List[ChannelEntry],
        new_channels: List[ChannelEntry],
        start_channel: int = 0,
        max_channels: int = 128,
        overwrite: bool = False,
        deduplicate: bool = True,
    ) -> List[ChannelEntry]:
        """Merges new channel entries into existing channels without slot collisions.

        Args:
            existing_channels: List of existing radio channels to preserve.
            new_channels: List of new candidate channels to insert.
            start_channel: Lowest channel slot index for new channel allocation.
            max_channels: Upper limit on total memory channels (128 for BF-F8HP).
            overwrite: If True, existing channels may be overwritten at identical slots.
            deduplicate: If True, skips channels with identical frequency + duplex + offset + tone.

        Returns:
            List of merged ChannelEntry objects sorted by location (0..max_channels-1).
        """
        allocated_map: Dict[int, ChannelEntry] = {}
        seen_signatures: Set[Tuple[float, str, float, float, str]] = set()

        # 1. Place existing channels into allocation map
        for ch in existing_channels:
            if 0 <= ch.location < max_channels:
                allocated_map[ch.location] = ch
                if deduplicate:
                    sig = (
                        round(ch.frequency, 4),
                        ch.duplex,
                        round(ch.offset, 4),
                        round(ch.r_tone_freq, 1),
                        ch.tone,
                    )
                    seen_signatures.add(sig)

        # 2. Iterate through new channels and allocate unoccupied slots
        current_slot = start_channel
        for ch in new_channels:
            if len(allocated_map) >= max_channels:
                break

            if deduplicate:
                sig = (
                    round(ch.frequency, 4),
                    ch.duplex,
                    round(ch.offset, 4),
                    round(ch.r_tone_freq, 1),
                    ch.tone,
                )
                if sig in seen_signatures:
                    continue
                seen_signatures.add(sig)

            # Determine target slot for the new channel
            target_slot: Optional[int] = None

            if not overwrite:
                # Check if requested location is available and >= start_channel
                if ch.location >= start_channel and ch.location not in allocated_map and ch.location < max_channels:
                    target_slot = ch.location
                else:
                    # Find next free slot >= start_channel
                    while current_slot < max_channels and current_slot in allocated_map:
                        current_slot += 1
                    if current_slot < max_channels:
                        target_slot = current_slot
                        current_slot += 1
            else:
                # Overwrite mode
                target_slot = ch.location if ch.location < max_channels else current_slot

            if target_slot is not None and 0 <= target_slot < max_channels:
                # Clone entry with updated location
                entry = ChannelEntry(
                    location=target_slot,
                    name=self.sanitize_channel_name(ch.name),
                    frequency=ch.frequency,
                    duplex=ch.duplex,
                    offset=ch.offset,
                    tone=ch.tone,
                    r_tone_freq=ch.r_tone_freq,
                    c_tone_freq=ch.c_tone_freq,
                    dtcs_code=ch.dtcs_code,
                    dtcs_polarity=ch.dtcs_polarity,
                    rx_dtcs_code=ch.rx_dtcs_code,
                    cross_mode=ch.cross_mode,
                    mode=ch.mode,
                    tstep=ch.tstep,
                    skip=ch.skip,
                    power=ch.power,
                    comment=ch.comment,
                    urcall=ch.urcall,
                    rpt1call=ch.rpt1call,
                    rpt2call=ch.rpt2call,
                    dvcode=ch.dvcode,
                )
                allocated_map[target_slot] = entry

        # Return sorted list of allocated channels
        merged_list = [allocated_map[loc] for loc in sorted(allocated_map.keys())]
        return merged_list[:max_channels]

    def validate_csv_file(self, csv_path: Path) -> Tuple[bool, List[str]]:
        """Validates a CHIRP CSV file against Baofeng BF-F8HP hardware and CHIRP schema constraints.

        Args:
            csv_path: Path to the CSV file to validate.

        Returns:
            Tuple of (is_valid, list_of_error_strings).
        """
        path = Path(csv_path).resolve()
        if not path.exists():
            return False, [f"File not found: {path}"]

        errors: List[str] = []

        try:
            with open(path, mode="r", newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return False, ["CSV file is empty"]

                clean_headers = [h.strip() for h in header]
                if len(clean_headers) < 19:
                    errors.append(f"Header has {len(clean_headers)} columns, expected at least 19")

                if clean_headers[:4] != ["Location", "Name", "Frequency", "Duplex"]:
                    errors.append(f"Header prefix mismatch: {clean_headers[:4]}")

                locations_seen: Set[int] = set()
                row_idx = 1

                for row in reader:
                    row_idx += 1
                    if not row or not any(row):
                        continue

                    if len(row) < 19:
                        errors.append(f"Row {row_idx}: expected at least 19 columns, got {len(row)}")
                        continue

                    # Validate location
                    try:
                        loc = int(row[0])
                        if not self.is_valid_channel_location(loc):
                            errors.append(f"Row {row_idx}: location {loc} out of bounds (0..127)")
                        if loc in locations_seen:
                            errors.append(f"Row {row_idx}: duplicate channel location {loc}")
                        locations_seen.add(loc)
                    except ValueError:
                        errors.append(f"Row {row_idx}: invalid integer location '{row[0]}'")

                    # Validate name
                    name = row[1].strip()
                    if len(name) > 7:
                        errors.append(f"Row {row_idx}: name '{name}' exceeds 7 characters")

                    # Validate frequency
                    try:
                        freq = float(row[2])
                        if not self.is_valid_frequency(freq):
                            errors.append(f"Row {row_idx}: frequency {freq:.6f} MHz out of VHF/UHF bounds")
                    except ValueError:
                        errors.append(f"Row {row_idx}: invalid float frequency '{row[2]}'")

                    # Validate duplex
                    duplex = row[3].strip()
                    if duplex not in VALID_DUPLEX:
                        errors.append(f"Row {row_idx}: invalid duplex '{duplex}'")

                    # Validate power
                    if len(row) > 13:
                        power = row[13].strip()
                        if power and power not in VALID_POWER:
                            errors.append(f"Row {row_idx}: invalid power level '{power}'")

        except Exception as exc:
            return False, [f"CSV parsing error: {exc}"]

        return len(errors) == 0, errors
