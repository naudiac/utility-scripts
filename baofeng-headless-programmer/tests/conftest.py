"""
Pytest configuration and shared fixtures for baofeng-headless-programmer tests.

Provides:
- Syspath setup to ensure skill scripts are importable.
- Mock RepeaterBook API responses for test zip codes (e.g. 30445).
- Mock Zippopotam geocoding responses.
- Synthetic binary radio memory images (BF-F8HP 128-channel format).
- Sample ChannelEntry, RepeaterInfo, and GeoLocation objects.
- Temporary directory fixtures and mock subprocess runners.
"""

import os
import sys
import json
import struct
import pytest
from pathlib import Path
from typing import List, Dict, Any

# Ensure skill scripts directory is on sys.path
SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Try importing domain models if available, otherwise define lightweight fallbacks for tests
try:
    from models import ChannelEntry, RepeaterInfo, GeoLocation, SubprocessResult
except ImportError:
    from dataclasses import dataclass, field

    @dataclass
    class ChannelEntry:
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

    @dataclass
    class RepeaterInfo:
        callsign: str
        frequency: float
        offset: float
        duplex: str
        tone_mode: str
        tone_freq: float
        dcs_code: str
        city: str
        state: str
        distance_miles: float
        on_air: bool = True
        ares: bool = False
        races: bool = False
        skywarn: bool = False
        linked: bool = False
        comment: str = ""
        mode: str = "FM"

    @dataclass
    class GeoLocation:
        zip_code: str
        city: str
        state: str
        state_abbr: str
        latitude: float
        longitude: float
        county: str = ""

    @dataclass
    class SubprocessResult:
        returncode: int
        stdout: str
        stderr: str
        command: List[str] = field(default_factory=list)


@pytest.fixture
def sample_zip_30445() -> str:
    return "30445"


@pytest.fixture
def mock_geoloc_30445() -> GeoLocation:
    return GeoLocation(
        zip_code="30445",
        city="Metter",
        state="Georgia",
        state_abbr="GA",
        latitude=32.397,
        longitude=-81.979,
        county="Candler"
    )


@pytest.fixture
def sample_repeaters_30445() -> List[RepeaterInfo]:
    return [
        RepeaterInfo(
            callsign="K4GAS",
            frequency=146.940,
            offset=0.600,
            duplex="-",
            tone_mode="Tone",
            tone_freq=100.0,
            dcs_code="023",
            city="Statesboro",
            state="GA",
            distance_miles=15.2,
            on_air=True,
            ares=True,
            races=False,
            skywarn=True,
            linked=True,
            comment="Statesboro ARC 2m Repeater (ARES/SKYWARN)"
        ),
        RepeaterInfo(
            callsign="W4MTR",
            frequency=444.800,
            offset=5.000,
            duplex="+",
            tone_mode="Tone",
            tone_freq=141.3,
            dcs_code="023",
            city="Metter",
            state="GA",
            distance_miles=2.1,
            on_air=True,
            ares=True,
            races=True,
            skywarn=False,
            linked=False,
            comment="Metter 70cm Repeater"
        ),
        RepeaterInfo(
            callsign="W4VDA",
            frequency=147.240,
            offset=0.600,
            duplex="+",
            tone_mode="Tone",
            tone_freq=100.0,
            dcs_code="023",
            city="Vidalia",
            state="GA",
            distance_miles=22.8,
            on_air=True,
            ares=False,
            races=False,
            skywarn=True,
            linked=False,
            comment="Vidalia 2m Repeater"
        ),
        RepeaterInfo(
            callsign="WR4A",
            frequency=145.450,
            offset=0.600,
            duplex="-",
            tone_mode="Tone",
            tone_freq=107.2,
            dcs_code="023",
            city="Swainsboro",
            state="GA",
            distance_miles=18.5,
            on_air=True,
            ares=False,
            races=False,
            skywarn=False,
            linked=False,
            comment="Swainsboro 2m Repeater"
        ),
        RepeaterInfo(
            callsign="K4GSO",
            frequency=146.880,
            offset=0.600,
            duplex="-",
            tone_mode="Tone",
            tone_freq=100.0,
            dcs_code="023",
            city="Dublin",
            state="GA",
            distance_miles=34.0,
            on_air=True,
            ares=True,
            races=False,
            skywarn=True,
            linked=True,
            comment="Dublin ARC 2m Repeater"
        ),
        RepeaterInfo(
            callsign="OFFLINE1",
            frequency=146.550,
            offset=0.600,
            duplex="-",
            tone_mode="Tone",
            tone_freq=100.0,
            dcs_code="023",
            city="Metter",
            state="GA",
            distance_miles=5.0,
            on_air=False,
            ares=False,
            races=False,
            skywarn=False,
            linked=False,
            comment="Decommissioned repeater"
        ),
    ]


@pytest.fixture
def mock_zippopotam_30445_json() -> Dict[str, Any]:
    return {
        "post code": "30445",
        "country": "United States",
        "country abbreviation": "US",
        "places": [
            {
                "place name": "Metter",
                "longitude": "-81.979",
                "state": "Georgia",
                "state abbreviation": "GA",
                "latitude": "32.397"
            }
        ]
    }


@pytest.fixture
def mock_repeaterbook_30445_json() -> List[Dict[str, Any]]:
    return [
        {
            "State ID": "13",
            "Repeater ID": "1001",
            "Frequency": "146.9400",
            "Input Freq": "146.3400",
            "PL": "100.0",
            "TSQ": "100.0",
            "Nearest City": "Statesboro",
            "Landmark": "Bulloch Tower",
            "County": "Bulloch",
            "State": "Georgia",
            "Callsign": "K4GAS",
            "Use": "OPEN",
            "Operational Status": "On-air",
            "ARES": "Yes",
            "RACES": "No",
            "SKYWARN": "Yes",
            "Operating Mode": "FM",
            "Analog Capable": "Yes",
            "Notes": "Statesboro Amateur Radio Club"
        },
        {
            "State ID": "13",
            "Repeater ID": "1002",
            "Frequency": "444.8000",
            "Input Freq": "449.8000",
            "PL": "141.3",
            "TSQ": "141.3",
            "Nearest City": "Metter",
            "Landmark": "Candler Tower",
            "County": "Candler",
            "State": "Georgia",
            "Callsign": "W4MTR",
            "Use": "OPEN",
            "Operational Status": "On-air",
            "ARES": "Yes",
            "RACES": "Yes",
            "SKYWARN": "No",
            "Operating Mode": "FM",
            "Analog Capable": "Yes",
            "Notes": "Metter 70cm Repeater"
        },
        {
            "State ID": "13",
            "Repeater ID": "1003",
            "Frequency": "147.2400",
            "Input Freq": "147.8400",
            "PL": "100.0",
            "TSQ": "100.0",
            "Nearest City": "Vidalia",
            "Landmark": "Toombs Tower",
            "County": "Toombs",
            "State": "Georgia",
            "Callsign": "W4VDA",
            "Use": "OPEN",
            "Operational Status": "On-air",
            "ARES": "No",
            "RACES": "No",
            "SKYWARN": "Yes",
            "Operating Mode": "FM",
            "Analog Capable": "Yes",
            "Notes": "Vidalia 2m Repeater"
        },
        {
            "State ID": "13",
            "Repeater ID": "1004",
            "Frequency": "146.5500",
            "Input Freq": "145.9500",
            "PL": "100.0",
            "TSQ": "100.0",
            "Nearest City": "Metter",
            "Landmark": "Old Tower",
            "County": "Candler",
            "State": "Georgia",
            "Callsign": "OFFLINE1",
            "Use": "CLOSED",
            "Operational Status": "Off-air",
            "ARES": "No",
            "RACES": "No",
            "SKYWARN": "No",
            "Operating Mode": "FM",
            "Analog Capable": "Yes",
            "Notes": "Decommissioned repeater"
        }
    ]


@pytest.fixture
def synthetic_radio_img(tmp_path: Path) -> Path:
    """Generates a synthetic 0x2000 byte Baofeng BF-F8HP memory image."""
    img_path = tmp_path / "synthetic_f8hp.img"
    # Create 8KB image filled with 0xFF (standard blank EEPROM)
    raw_data = bytearray(b"\xFF" * 0x2000)
    
    # Write magic header / firmware ident at aux block 0x1EC0
    firmware_ident = b"HN5RV01" + b"\x00" * 9
    raw_data[0x1EC0:0x1ED0] = firmware_ident
    
    img_path.write_bytes(bytes(raw_data))
    return img_path


@pytest.fixture
def sample_existing_channels() -> List[ChannelEntry]:
    """Returns sample channels occupying slots 0..4."""
    return [
        ChannelEntry(
            location=0,
            name="CALL-2M",
            frequency=146.520000,
            duplex="",
            offset=0.000000,
            tone="",
            mode="FM",
            power="High",
            comment="National Simplex Calling"
        ),
        ChannelEntry(
            location=1,
            name="LOC-SMP",
            frequency=146.550000,
            duplex="",
            offset=0.000000,
            tone="",
            mode="FM",
            power="High",
            comment="Local Club Simplex"
        ),
        ChannelEntry(
            location=2,
            name="CALL70C",
            frequency=446.000000,
            duplex="",
            offset=0.000000,
            tone="",
            mode="FM",
            power="High",
            comment="70cm Simplex Calling"
        ),
        ChannelEntry(
            location=3,
            name="SAR-PRI",
            frequency=155.160000,
            duplex="",
            offset=0.000000,
            tone="",
            mode="FM",
            power="Low",
            comment="National Search and Rescue"
        ),
        ChannelEntry(
            location=4,
            name="RED-CRS",
            frequency=153.740000,
            duplex="",
            offset=0.000000,
            tone="",
            mode="FM",
            power="Low",
            comment="Red Cross Disaster"
        )
    ]
