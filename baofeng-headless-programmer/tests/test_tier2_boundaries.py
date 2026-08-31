"""
Tier 2: Boundary & Corner Case Test Suite.

Covers:
- Zero-repeater isolation & rural sparse coverage
- Exact 128-channel capacity boundaries (0, 127, 128, overflow)
- 7-character LCD alphanumeric name truncation & sanitization edge cases
- VHF/UHF frequency band limits (136-174 MHz, 400-520 MHz) & out-of-band rejection
- CTCSS sub-audible tone boundaries (67.0 Hz - 254.1 Hz)
- DCS code formatting & zero-padding (023 - 754)
- US Zip Code validation boundaries (4-digit, 6-digit, alpha, 00000)
- Search radius boundaries (1 mile - 100 miles, negative radius)
- Duplex offset bounds (0.0 MHz - 70.0 MHz)
"""

import pytest
from pathlib import Path
from typing import List

try:
    from models import ChannelEntry, RepeaterInfo, GeoLocation
    from csv_engine import CSVEngine
    from frequency_fetcher import FrequencyFetcher
    from chirp_driver import ChirpDriver
except ImportError:
    pass


class TestZeroRepeaterIsolationBoundary:
    def test_boundary_zero_repeaters_returns_empty_list(self):
        fetcher = FrequencyFetcher()
        result = fetcher.parse_repeaterbook_response([])
        assert result == []

    def test_boundary_zero_repeaters_frequency_plan_contains_noaa_and_gmrs(self):
        fetcher = FrequencyFetcher()
        # Build plan with 0 repeaters
        plan = fetcher.build_frequency_plan_from_components(
            repeaters=[],
            include_noaa=True,
            include_gmrs=True,
            include_calling=True
        )
        assert len(plan) == 7 + 22 + 1  # 30 channels
        assert any(ch.frequency == 146.520 for ch in plan)
        assert sum(1 for ch in plan if "WX" in ch.name or "NOAA" in ch.comment) == 7


class TestChannelCapacity128Boundaries:
    def test_boundary_channel_index_min_zero(self):
        ch = ChannelEntry(location=0, name="CH0", frequency=146.520)
        assert ch.location == 0

    def test_boundary_channel_index_max_127(self):
        ch = ChannelEntry(location=127, name="CH127", frequency=146.520)
        assert ch.location == 127

    def test_boundary_channel_index_128_out_of_bounds_validation(self):
        csv_engine = CSVEngine()
        ch = ChannelEntry(location=128, name="CH128", frequency=146.520)
        assert csv_engine.is_valid_channel_location(ch.location) is False

    def test_boundary_channel_index_negative_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_channel_location(-1) is False

    def test_boundary_exact_128_channels_merge(self):
        csv_engine = CSVEngine()
        channels = [
            ChannelEntry(location=i, name=f"C{i:03d}", frequency=146.0 + (i * 0.01))
            for i in range(128)
        ]
        merged = csv_engine.merge_channels([], channels, max_channels=128)
        assert len(merged) == 128
        assert merged[0].location == 0
        assert merged[-1].location == 127

    def test_boundary_129_channels_capped_at_128(self):
        csv_engine = CSVEngine()
        channels = [
            ChannelEntry(location=i, name=f"C{i:03d}", frequency=146.0 + (i * 0.01))
            for i in range(129)
        ]
        merged = csv_engine.merge_channels([], channels, max_channels=128)
        assert len(merged) == 128
        assert all(ch.location < 128 for ch in merged)

    def test_boundary_250_repeaters_overflow_capping(self):
        csv_engine = CSVEngine()
        channels = [
            ChannelEntry(location=i, name=f"C{i:03d}", frequency=146.0 + (i * 0.005))
            for i in range(250)
        ]
        merged = csv_engine.merge_channels([], channels, max_channels=128)
        assert len(merged) == 128


class TestDisplayName7CharacterBoundaries:
    def test_boundary_name_exact_7_characters(self):
        csv_engine = CSVEngine()
        name = "STATESB"
        assert csv_engine.sanitize_channel_name(name) == "STATESB"

    def test_boundary_name_8_characters_truncated(self):
        csv_engine = CSVEngine()
        name = "STATESBO"
        assert csv_engine.sanitize_channel_name(name) == "STATESB"

    def test_boundary_name_20_characters_truncated(self):
        csv_engine = CSVEngine()
        name = "STATESBORO-REPEATER-2M"
        assert csv_engine.sanitize_channel_name(name) == "STATESB"

    def test_boundary_name_single_character(self):
        csv_engine = CSVEngine()
        name = "K"
        assert csv_engine.sanitize_channel_name(name) == "K"

    def test_boundary_name_empty_string(self):
        csv_engine = CSVEngine()
        assert csv_engine.sanitize_channel_name("") == ""

    def test_boundary_name_special_symbols_filtered(self):
        csv_engine = CSVEngine()
        # Should strip non-alphanumeric except hyphen or space
        assert csv_engine.sanitize_channel_name("K4!@#$G") == "K4G"

    def test_boundary_name_whitespace_handling(self):
        csv_engine = CSVEngine()
        assert csv_engine.sanitize_channel_name("WX 1") == "WX 1"


class TestFrequencyBandBoundaries:
    def test_boundary_vhf_lower_limit_136_000(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(136.000000) is True

    def test_boundary_vhf_upper_limit_174_000(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(174.000000) is True

    def test_boundary_uhf_lower_limit_400_000(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(400.000000) is True

    def test_boundary_uhf_upper_limit_520_000(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(520.000000) is True

    def test_boundary_vhf_just_below_136_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(135.999999) is False

    def test_boundary_vhf_just_above_174_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(174.000001) is False

    def test_boundary_uhf_just_below_400_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(399.999999) is False

    def test_boundary_uhf_just_above_520_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(520.000001) is False

    def test_boundary_220mhz_band_rejected_for_f8hp(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(222.500000) is False

    def test_boundary_900mhz_band_rejected(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(902.500000) is False


class TestToneAndSquelchBoundaries:
    def test_boundary_ctcss_min_tone_67_0(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_ctcss_tone(67.0) is True

    def test_boundary_ctcss_max_tone_254_1(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_ctcss_tone(254.1) is True

    def test_boundary_ctcss_below_min_rejected(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_ctcss_tone(60.0) is False

    def test_boundary_ctcss_above_max_rejected(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_ctcss_tone(260.0) is False

    def test_boundary_dtcs_code_padding_023(self):
        csv_engine = CSVEngine()
        assert csv_engine.format_dtcs_code("23") == "023"
        assert csv_engine.format_dtcs_code(23) == "023"

    def test_boundary_dtcs_code_max_754(self):
        csv_engine = CSVEngine()
        assert csv_engine.format_dtcs_code("754") == "754"


class TestZipCodeAndRadiusBoundaries:
    def test_boundary_zip_code_4_digits_invalid(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_zip_code("3044") is False

    def test_boundary_zip_code_6_digits_invalid(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_zip_code("304455") is False

    def test_boundary_zip_code_alphanumeric_invalid(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_zip_code("3044A") is False

    def test_boundary_zip_code_valid_5_digits(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_zip_code("30445") is True

    def test_boundary_radius_min_1_mile(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_radius(1.0) is True

    def test_boundary_radius_max_100_miles(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_radius(100.0) is True

    def test_boundary_radius_zero_or_negative_rejected(self):
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_radius(0.0) is False
        assert fetcher.is_valid_radius(-10.0) is False


class TestDuplexAndOffsetBoundaries:
    def test_boundary_offset_zero_for_simplex(self):
        ch = ChannelEntry(location=0, name="SMP", frequency=146.520, duplex="", offset=0.0)
        assert ch.offset == 0.0
        assert ch.duplex == ""

    def test_boundary_offset_max_70mhz(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_offset(70.0) is True
        assert csv_engine.is_valid_offset(70.1) is False
        assert csv_engine.is_valid_offset(-0.1) is False
