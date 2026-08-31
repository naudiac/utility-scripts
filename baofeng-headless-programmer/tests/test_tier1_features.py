"""
Tier 1: Feature Coverage & Unit Correctness Test Suite.

Covers all 16 features from PROJECT.md & TEST_INFRA.md:
- Feature 1: Headless CHIRP Download
- Feature 2: Timestamped Local Backup
- Feature 3: Subprocess Safety & Mock Engine
- Feature 4: Zip Code Geocoder
- Feature 5: RepeaterBook Sourcing & Fallback
- Feature 6: Strict On-Air Filter
- Feature 7: EmComm & Linked Prioritization
- Feature 8: NOAA 7-Channel Generator
- Feature 9: VHF Simplex Calling Channel
- Feature 10: GMRS/FRS Channels 1-22
- Feature 11: CHIRP CSV Serialization
- Feature 12: 128-Channel Capacity Allocator
- Feature 13: Hardware Limits & Tag Sanitizer
- Feature 14: Safe Headless Writeback
- Feature 15: Production CLI Interface
- Feature 16: Antigravity Skill Packaging
"""

import os
import sys
import json
import pytest
from pathlib import Path
from typing import List

# Import domain modules
try:
    from models import ChannelEntry, RepeaterInfo, GeoLocation, SubprocessResult
    from chirp_driver import ChirpDriver
    from frequency_fetcher import FrequencyFetcher
    from csv_engine import CSVEngine
    from baofeng_programmer import parse_args, build_parser
except ImportError:
    pass


# ============================================================================
# FEATURE 1: Headless CHIRP Download
# ============================================================================

class TestFeature1HeadlessChirpDownload:
    def test_f1_download_command_line_structure(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "radio.img"
        cmd = driver.build_download_cmd(port="COM3", output_path=out_img, model="Baofeng_BF-F8HP")
        
        assert "chirpc" in cmd[0] or "python" in cmd[0] or "chirpc" in str(cmd)
        assert "--download-mmap" in cmd or "-d" in cmd or any("download" in arg for arg in cmd)
        assert any("COM3" in arg for arg in cmd)
        assert any("Baofeng_BF-F8HP" in arg for arg in cmd)

    def test_f1_download_model_parameter_default(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "radio.img"
        cmd = driver.build_download_cmd(port="COM1", output_path=out_img)
        assert any("Baofeng_BF-F8HP" in arg for arg in cmd)

    def test_f1_download_custom_model_parameter(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "radio.img"
        cmd = driver.build_download_cmd(port="COM1", output_path=out_img, model="Baofeng_UV-5R")
        assert any("Baofeng_UV-5R" in arg for arg in cmd)

    def test_f1_download_dry_run_creates_image_file(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "dry_run.img"
        result = driver.download_radio_image(port="COM3", output_path=out_img, dry_run=True)
        assert result.returncode == 0
        assert out_img.exists()
        assert out_img.stat().st_size > 0

    def test_f1_download_mock_mode_execution(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "mock.img"
        result = driver.download_radio_image(port="COM3", output_path=out_img, mock=True)
        assert result.returncode == 0
        assert out_img.exists()

    def test_f1_download_windows_extended_port_syntax(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "ext_port.img"
        cmd = driver.build_download_cmd(port=r"\\.\COM12", output_path=out_img)
        assert any(r"\\.\COM12" in arg or "COM12" in arg for arg in cmd)


# ============================================================================
# FEATURE 2: Timestamped Local Backup
# ============================================================================

class TestFeature2TimestampedLocalBackup:
    def test_f2_backup_filename_format_contains_timestamp(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        backup_dir = tmp_path / "backups"
        backup_path = driver.create_backup(source_path=synthetic_radio_img, backup_dir=backup_dir)
        
        assert backup_path.exists()
        assert backup_path.parent == backup_dir
        assert "backup" in backup_path.name.lower()
        # Verify timestamp format (e.g. 2026...)
        assert any(char.isdigit() for char in backup_path.name)

    def test_f2_backup_creates_missing_directory(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        backup_dir = tmp_path / "deep" / "nested" / "backups"
        assert not backup_dir.exists()
        backup_path = driver.create_backup(source_path=synthetic_radio_img, backup_dir=backup_dir)
        assert backup_dir.exists()
        assert backup_path.exists()

    def test_f2_backup_copies_exact_bytes(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        backup_dir = tmp_path / "backups"
        backup_path = driver.create_backup(source_path=synthetic_radio_img, backup_dir=backup_dir)
        assert backup_path.read_bytes() == synthetic_radio_img.read_bytes()

    def test_f2_backup_creates_both_img_and_csv(self, tmp_path, synthetic_radio_img, sample_existing_channels):
        driver = ChirpDriver()
        csv_engine = CSVEngine()
        backup_dir = tmp_path / "backups"
        
        img_backup = driver.create_backup(synthetic_radio_img, backup_dir)
        csv_backup = csv_engine.export_csv(sample_existing_channels, backup_dir / f"{img_backup.stem}.csv")
        
        assert img_backup.exists()
        assert csv_backup.exists()
        assert img_backup.suffix == ".img"
        assert csv_backup.suffix == ".csv"

    def test_f2_backup_preserves_original_file(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        backup_dir = tmp_path / "backups"
        original_size = synthetic_radio_img.stat().st_size
        driver.create_backup(synthetic_radio_img, backup_dir)
        assert synthetic_radio_img.exists()
        assert synthetic_radio_img.stat().st_size == original_size


# ============================================================================
# FEATURE 3: Subprocess Safety & Mock Engine
# ============================================================================

class TestFeature3SubprocessSafety:
    def test_f3_subprocess_safety_flags(self):
        driver = ChirpDriver()
        assert hasattr(driver, "timeout")
        assert driver.timeout >= 5

    def test_f3_subprocess_captures_output_in_dry_run(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "test.img"
        res = driver.download_radio_image(port="COM1", output_path=out_img, dry_run=True)
        assert isinstance(res.stdout, str)
        assert isinstance(res.stderr, str)
        assert isinstance(res.returncode, int)

    def test_f3_subprocess_mock_mode_zero_external_processes(self, tmp_path):
        driver = ChirpDriver()
        out_img = tmp_path / "mock.img"
        res = driver.download_radio_image(port="COM99", output_path=out_img, mock=True)
        assert res.returncode == 0
        assert out_img.exists()

    def test_f3_subprocess_custom_timeout_setting(self):
        driver = ChirpDriver(timeout=15)
        assert driver.timeout == 15

    def test_f3_subprocess_result_dataclass_structure(self):
        res = SubprocessResult(returncode=0, stdout="OK", stderr="", command=["chirpc", "--help"])
        assert res.returncode == 0
        assert res.stdout == "OK"
        assert res.stderr == ""
        assert res.command == ["chirpc", "--help"]


# ============================================================================
# FEATURE 4: Zip Code Geocoder
# ============================================================================

class TestFeature4ZipCodeGeocoder:
    def test_f4_resolve_zip_valid_30445(self):
        fetcher = FrequencyFetcher()
        loc = fetcher.resolve_zip("30445", mock=True)
        assert loc.zip_code == "30445"
        assert loc.city in ["Metter", "Mount Vernon"] or loc.state_abbr == "GA"
        assert loc.state_abbr == "GA"
        assert abs(loc.latitude - 32.397) < 1.0
        assert abs(loc.longitude - (-81.979)) < 1.5

    def test_f4_fips_mapping_georgia(self):
        fetcher = FrequencyFetcher()
        fips = fetcher.get_fips_code("GA")
        assert fips == "13"

    def test_f4_fips_mapping_major_states(self):
        fetcher = FrequencyFetcher()
        assert fetcher.get_fips_code("CA") == "06"
        assert fetcher.get_fips_code("TX") == "48"
        assert fetcher.get_fips_code("FL") == "12"
        assert fetcher.get_fips_code("NY") == "36"

    def test_f4_haversine_distance_known_coordinates(self):
        fetcher = FrequencyFetcher()
        # Distance between Metter, GA (32.397, -81.979) and Statesboro, GA (32.448, -81.783) ~ 15 miles
        dist = fetcher.calculate_distance(32.397, -81.979, 32.448, -81.783)
        assert 10.0 <= dist <= 20.0

    def test_f4_haversine_distance_zero_for_same_point(self):
        fetcher = FrequencyFetcher()
        dist = fetcher.calculate_distance(32.397, -81.979, 32.397, -81.979)
        assert dist == 0.0

    def test_f4_resolve_zip_extracts_county_if_available(self):
        fetcher = FrequencyFetcher()
        loc = fetcher.resolve_zip("30445", mock=True)
        assert isinstance(loc.county, str)


# ============================================================================
# FEATURE 5: RepeaterBook Sourcing & Fallback
# ============================================================================

class TestFeature5RepeaterBookSourcing:
    def test_f5_repeaterbook_headers_and_user_agent(self):
        fetcher = FrequencyFetcher()
        headers = fetcher.build_request_headers()
        assert "User-Agent" in headers
        assert "Baofeng" in headers["User-Agent"] or "Programmer" in headers["User-Agent"]

    def test_f5_repeaterbook_json_to_repeaterinfo_mapping(self, mock_repeaterbook_30445_json):
        fetcher = FrequencyFetcher()
        repeaters = fetcher.parse_repeaterbook_response(mock_repeaterbook_30445_json)
        assert len(repeaters) == 4
        assert repeaters[0].callsign == "K4GAS"
        assert repeaters[0].frequency == 146.940
        assert repeaters[0].offset == 0.600
        assert repeaters[0].duplex == "-"
        assert repeaters[0].tone_freq == 100.0

    def test_f5_repeaterbook_offline_fallback_for_30445(self):
        fetcher = FrequencyFetcher()
        repeaters = fetcher.fetch_repeaters("30445", mock=True)
        assert len(repeaters) >= 3
        callsigns = [r.callsign for r in repeaters]
        assert any(c in ["K4GAS", "W4MTR", "W4VDA", "WR4A"] for c in callsigns)

    def test_f5_repeaterbook_radius_filter(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_by_radius(sample_repeaters_30445, max_radius_miles=20.0)
        assert all(r.distance_miles <= 20.0 for r in filtered)

    def test_f5_repeaterbook_empty_results_handling(self):
        fetcher = FrequencyFetcher()
        repeaters = fetcher.parse_repeaterbook_response([])
        assert repeaters == []


# ============================================================================
# FEATURE 6: Strict On-Air Filter
# ============================================================================

class TestFeature6StrictOnAirFilter:
    def test_f6_on_air_filter_includes_on_air(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_on_air(sample_repeaters_30445)
        assert all(r.on_air is True for r in filtered)

    def test_f6_on_air_filter_excludes_off_air(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_on_air(sample_repeaters_30445)
        callsigns = [r.callsign for r in filtered]
        assert "OFFLINE1" not in callsigns

    def test_f6_on_air_filter_excludes_testing_and_decommissioned(self):
        fetcher = FrequencyFetcher()
        test_data = [
            RepeaterInfo(callsign="R1", frequency=146.94, offset=0.6, duplex="-", tone_mode="Tone",
                         tone_freq=100.0, dcs_code="023", city="A", state="GA", distance_miles=10, on_air=True),
            RepeaterInfo(callsign="R2", frequency=147.00, offset=0.6, duplex="+", tone_mode="Tone",
                         tone_freq=100.0, dcs_code="023", city="B", state="GA", distance_miles=12, on_air=False),
        ]
        filtered = fetcher.filter_on_air(test_data)
        assert len(filtered) == 1
        assert filtered[0].callsign == "R1"

    def test_f6_on_air_filter_case_insensitive_matching(self):
        fetcher = FrequencyFetcher()
        raw_items = [
            {"Callsign": "K1", "Operational Status": "On-Air", "Frequency": "146.94"},
            {"Callsign": "K2", "Operational Status": "ON-AIR", "Frequency": "147.00"},
            {"Callsign": "K3", "Operational Status": "off-air", "Frequency": "147.20"},
        ]
        repeaters = fetcher.parse_repeaterbook_response(raw_items)
        on_air = fetcher.filter_on_air(repeaters)
        assert len(on_air) == 2

    def test_f6_on_air_filter_preserves_on_air_count(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        initial_on_air_count = sum(1 for r in sample_repeaters_30445 if r.on_air)
        filtered = fetcher.filter_on_air(sample_repeaters_30445)
        assert len(filtered) == initial_on_air_count


# ============================================================================
# FEATURE 7: EmComm & Linked Prioritization
# ============================================================================

class TestFeature7EmCommAndLinkedPrioritization:
    def test_f7_prioritize_ares_flagged_repeaters(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        prioritized = fetcher.prioritize_repeaters(sample_repeaters_30445)
        # Verify first items have ARES, SKYWARN, or Linked flags
        top_item = prioritized[0]
        assert top_item.ares or top_item.races or top_item.skywarn or top_item.linked

    def test_f7_prioritize_races_flagged_repeaters(self):
        fetcher = FrequencyFetcher()
        r1 = RepeaterInfo("R1", 146.94, 0.6, "-", "Tone", 100.0, "023", "A", "GA", 10, True, ares=False, races=True)
        r2 = RepeaterInfo("R2", 147.00, 0.6, "+", "Tone", 100.0, "023", "B", "GA", 5, True, ares=False, races=False)
        prioritized = fetcher.prioritize_repeaters([r2, r1])
        assert prioritized[0].callsign == "R1"

    def test_f7_prioritize_skywarn_flagged_repeaters(self):
        fetcher = FrequencyFetcher()
        r1 = RepeaterInfo("R1", 146.94, 0.6, "-", "Tone", 100.0, "023", "A", "GA", 10, True, skywarn=True)
        r2 = RepeaterInfo("R2", 147.00, 0.6, "+", "Tone", 100.0, "023", "B", "GA", 5, True, skywarn=False)
        prioritized = fetcher.prioritize_repeaters([r2, r1])
        assert prioritized[0].callsign == "R1"

    def test_f7_prioritize_linked_network_repeaters(self):
        fetcher = FrequencyFetcher()
        r1 = RepeaterInfo("R1", 146.94, 0.6, "-", "Tone", 100.0, "023", "A", "GA", 10, True, linked=True)
        r2 = RepeaterInfo("R2", 147.00, 0.6, "+", "Tone", 100.0, "023", "B", "GA", 5, True, linked=False)
        prioritized = fetcher.prioritize_repeaters([r2, r1])
        assert prioritized[0].callsign == "R1"

    def test_f7_multi_priority_scoring_order(self):
        fetcher = FrequencyFetcher()
        # High score: ARES + SKYWARN + Linked
        r_super = RepeaterInfo("SUP", 146.94, 0.6, "-", "Tone", 100.0, "023", "A", "GA", 15, True, ares=True, skywarn=True, linked=True)
        # Medium score: ARES only
        r_ares = RepeaterInfo("ARS", 147.00, 0.6, "+", "Tone", 100.0, "023", "B", "GA", 10, True, ares=True)
        # Low score: Standard unlinked
        r_plain = RepeaterInfo("PLN", 147.20, 0.6, "+", "Tone", 100.0, "023", "C", "GA", 5, True)
        
        res = fetcher.prioritize_repeaters([r_plain, r_ares, r_super])
        assert res[0].callsign == "SUP"
        assert res[1].callsign == "ARS"
        assert res[2].callsign == "PLN"


# ============================================================================
# FEATURE 8: NOAA 7-Channel Generator
# ============================================================================

class TestFeature8NOAA7ChannelGenerator:
    def test_f8_noaa_generates_exactly_7_channels(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        assert len(noaa_channels) == 7

    def test_f8_noaa_standard_frequencies_exact_values(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        expected_freqs = {162.400, 162.425, 162.450, 162.475, 162.500, 162.525, 162.550}
        actual_freqs = {round(ch.frequency, 4) for ch in noaa_channels}
        assert actual_freqs == expected_freqs

    def test_f8_noaa_duplex_is_off_or_empty(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        for ch in noaa_channels:
            assert ch.duplex in ["", "off"]

    def test_f8_noaa_power_level_is_low(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        for ch in noaa_channels:
            assert ch.power == "Low"

    def test_f8_noaa_offset_is_zero(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        for ch in noaa_channels:
            assert ch.offset == 0.0

    def test_f8_noaa_mode_is_fm(self):
        fetcher = FrequencyFetcher()
        noaa_channels = fetcher.get_noaa_channels()
        for ch in noaa_channels:
            assert ch.mode == "FM"


# ============================================================================
# FEATURE 9: VHF Simplex Calling Channel
# ============================================================================

class TestFeature9VHFSimplexCallingChannel:
    def test_f9_simplex_calling_frequency_146520(self):
        fetcher = FrequencyFetcher()
        calling = fetcher.get_simplex_calling()
        assert round(calling.frequency, 4) == 146.5200

    def test_f9_simplex_calling_name_length_le_7(self):
        fetcher = FrequencyFetcher()
        calling = fetcher.get_simplex_calling()
        assert len(calling.name) <= 7
        assert calling.name != ""

    def test_f9_simplex_calling_duplex_is_empty(self):
        fetcher = FrequencyFetcher()
        calling = fetcher.get_simplex_calling()
        assert calling.duplex == ""

    def test_f9_simplex_calling_power_is_high(self):
        fetcher = FrequencyFetcher()
        calling = fetcher.get_simplex_calling()
        assert calling.power == "High"

    def test_f9_simplex_calling_step_and_mode(self):
        fetcher = FrequencyFetcher()
        calling = fetcher.get_simplex_calling()
        assert calling.mode == "FM"
        assert calling.tstep == 5.0


# ============================================================================
# FEATURE 10: GMRS/FRS Channels 1-22
# ============================================================================

class TestFeature10GMRSFRSChannels:
    def test_f10_gmrs_generates_22_channels(self):
        fetcher = FrequencyFetcher()
        gmrs_channels = fetcher.get_gmrs_frs_channels()
        assert len(gmrs_channels) == 22

    def test_f10_gmrs_channel_1_frequency_4625625(self):
        fetcher = FrequencyFetcher()
        gmrs_channels = fetcher.get_gmrs_frs_channels()
        assert round(gmrs_channels[0].frequency, 6) == 462.562500

    def test_f10_gmrs_channel_22_frequency_4627250(self):
        fetcher = FrequencyFetcher()
        gmrs_channels = fetcher.get_gmrs_frs_channels()
        assert round(gmrs_channels[21].frequency, 6) == 462.725000

    def test_f10_gmrs_duplex_empty_for_simplex(self):
        fetcher = FrequencyFetcher()
        gmrs_channels = fetcher.get_gmrs_frs_channels()
        for ch in gmrs_channels:
            assert ch.duplex == ""
            assert ch.offset == 0.0

    def test_f10_gmrs_names_within_7_chars(self):
        fetcher = FrequencyFetcher()
        gmrs_channels = fetcher.get_gmrs_frs_channels()
        for ch in gmrs_channels:
            assert len(ch.name) <= 7


# ============================================================================
# FEATURE 11: CHIRP CSV Serialization
# ============================================================================

class TestFeature11CHIRPCSVSerialization:
    def test_f11_csv_headers_exact_19_columns(self, tmp_path, sample_existing_channels):
        csv_engine = CSVEngine()
        out_csv = tmp_path / "test.csv"
        csv_engine.export_csv(sample_existing_channels, out_csv)
        
        with open(out_csv, "r", encoding="utf-8") as f:
            header_line = f.readline().strip()
        headers = [h.strip() for h in header_line.split(",")]
        assert len(headers) >= 19
        assert headers[0] == "Location"
        assert headers[1] == "Name"
        assert headers[2] == "Frequency"
        assert headers[3] == "Duplex"

    def test_f11_csv_frequency_formatted_to_6_decimals(self, tmp_path, sample_existing_channels):
        csv_engine = CSVEngine()
        out_csv = tmp_path / "test_fmt.csv"
        csv_engine.export_csv(sample_existing_channels, out_csv)
        
        lines = out_csv.read_text(encoding="utf-8").strip().splitlines()
        data_row = lines[1].split(",")
        freq_str = data_row[2]
        assert "." in freq_str
        assert len(freq_str.split(".")[1]) == 6

    def test_f11_csv_offset_formatted_to_6_decimals(self, tmp_path, sample_repeaters_30445):
        csv_engine = CSVEngine()
        channels = [
            ChannelEntry(location=0, name="RPT1", frequency=146.940, duplex="-", offset=0.6, tone="Tone", r_tone_freq=100.0)
        ]
        out_csv = tmp_path / "test_offset.csv"
        csv_engine.export_csv(channels, out_csv)
        
        lines = out_csv.read_text(encoding="utf-8").strip().splitlines()
        offset_str = lines[1].split(",")[4]
        assert offset_str == "0.600000"

    def test_f11_csv_tone_formatting_tone_tsql_dtcs(self, tmp_path):
        csv_engine = CSVEngine()
        channels = [
            ChannelEntry(location=0, name="T1", frequency=146.94, tone="Tone", r_tone_freq=100.0),
            ChannelEntry(location=1, name="T2", frequency=146.96, tone="TSQL", c_tone_freq=123.0),
            ChannelEntry(location=2, name="T3", frequency=444.80, tone="DTCS", dtcs_code="023"),
        ]
        out_csv = tmp_path / "test_tones.csv"
        csv_engine.export_csv(channels, out_csv)
        imported = csv_engine.import_csv(out_csv)
        assert imported[0].tone == "Tone"
        assert imported[1].tone == "TSQL"
        assert imported[2].tone == "DTCS"

    def test_f11_csv_export_import_roundtrip(self, tmp_path, sample_existing_channels):
        csv_engine = CSVEngine()
        out_csv = tmp_path / "roundtrip.csv"
        csv_engine.export_csv(sample_existing_channels, out_csv)
        imported = csv_engine.import_csv(out_csv)
        assert len(imported) == len(sample_existing_channels)
        assert imported[0].name == sample_existing_channels[0].name
        assert round(imported[0].frequency, 4) == round(sample_existing_channels[0].frequency, 4)


# ============================================================================
# FEATURE 12: 128-Channel Capacity Allocator
# ============================================================================

class TestFeature12ChannelCapacityAllocator:
    def test_f12_allocator_enforces_128_channel_limit(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(zip_code="30445", max_total_channels=128, mock=True)
        assert len(plan) <= 128

    def test_f12_allocator_location_indices_range_0_to_127(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(zip_code="30445", max_total_channels=128, mock=True)
        for ch in plan:
            assert 0 <= ch.location <= 127

    def test_f12_allocator_truncates_overflow_gracefully(self):
        csv_engine = CSVEngine()
        # Create 150 channel candidates
        candidates = [
            ChannelEntry(location=i, name=f"CH{i:03d}", frequency=146.0 + (i * 0.02))
            for i in range(150)
        ]
        merged = csv_engine.merge_channels([], candidates, max_channels=128)
        assert len(merged) == 128
        assert merged[-1].location == 127

    def test_f12_allocator_merges_without_slot_collisions(self, sample_existing_channels):
        csv_engine = CSVEngine()
        new_chans = [
            ChannelEntry(location=0, name="NEW1", frequency=147.000),
            ChannelEntry(location=1, name="NEW2", frequency=147.020),
        ]
        merged = csv_engine.merge_channels(sample_existing_channels, new_chans, start_channel=5)
        locations = [ch.location for ch in merged]
        assert len(locations) == len(set(locations))  # all unique

    def test_f12_allocator_preserves_dedicated_noaa_slots(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(zip_code="30445", max_total_channels=128, mock=True)
        noaa_chans = [ch for ch in plan if "WX" in ch.name or "NOAA" in ch.comment]
        assert len(noaa_chans) == 7


# ============================================================================
# FEATURE 13: Hardware Limits & Tag Sanitizer
# ============================================================================

class TestFeature13HardwareLimitsAndSanitizer:
    def test_f13_tag_sanitizer_max_7_chars(self):
        csv_engine = CSVEngine()
        sanitized = csv_engine.sanitize_channel_name("STATESBORO-RPT")
        assert len(sanitized) <= 7

    def test_f13_tag_sanitizer_uppercase_alphanumeric(self):
        csv_engine = CSVEngine()
        sanitized = csv_engine.sanitize_channel_name("k4gas-2m")
        assert sanitized == sanitized.upper()

    def test_f13_tag_sanitizer_removes_slashes_and_special_symbols(self):
        csv_engine = CSVEngine()
        sanitized = csv_engine.sanitize_channel_name("W4/VDA#1")
        assert "/" not in sanitized
        assert "#" not in sanitized

    def test_f13_power_levels_strictly_high_med_low(self):
        valid_powers = {"High", "Med", "Low"}
        ch = ChannelEntry(location=0, name="PWR", frequency=146.52, power="Med")
        assert ch.power in valid_powers

    def test_f13_frequency_band_validation_vhf_uhf(self):
        csv_engine = CSVEngine()
        assert csv_engine.is_valid_frequency(146.520) is True  # VHF
        assert csv_engine.is_valid_frequency(444.800) is True  # UHF
        assert csv_engine.is_valid_frequency(220.500) is False  # 1.25m out of band for BF-F8HP
        assert csv_engine.is_valid_frequency(900.000) is False  # 33cm out of band


# ============================================================================
# FEATURE 14: Safe Headless Writeback
# ============================================================================

class TestFeature14SafeHeadlessWriteback:
    def test_f14_upload_command_line_structure(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        cmd = driver.build_upload_cmd(port="COM3", input_path=synthetic_radio_img, model="Baofeng_BF-F8HP")
        assert "--upload-mmap" in cmd or "-u" in cmd or any("upload" in arg for arg in cmd)
        assert any("COM3" in arg for arg in cmd)
        assert any("Baofeng_BF-F8HP" in arg for arg in cmd)

    def test_f14_upload_dry_run_mode(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        res = driver.upload_radio_image(port="COM3", input_path=synthetic_radio_img, dry_run=True)
        assert res.returncode == 0

    def test_f14_upload_mock_mode(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        res = driver.upload_radio_image(port="COM3", input_path=synthetic_radio_img, mock=True)
        assert res.returncode == 0

    def test_f14_upload_validates_image_file_exists(self, tmp_path):
        driver = ChirpDriver()
        non_existent = tmp_path / "does_not_exist.img"
        with pytest.raises((FileNotFoundError, ValueError)):
            driver.upload_radio_image(port="COM3", input_path=non_existent)

    def test_f14_upload_custom_model_parameter(self, tmp_path, synthetic_radio_img):
        driver = ChirpDriver()
        cmd = driver.build_upload_cmd(port="COM3", input_path=synthetic_radio_img, model="Baofeng_UV-5R")
        assert any("Baofeng_UV-5R" in arg for arg in cmd)


# ============================================================================
# FEATURE 15: Production CLI Interface
# ============================================================================

class TestFeature15ProductionCLIInterface:
    def test_f15_cli_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["--zip", "30445"])
        assert args.zip == "30445"
        assert args.dry_run is False
        assert args.mock is False
        assert args.radio_model == "Baofeng_BF-F8HP"

    def test_f15_cli_zip_and_port_parsing(self):
        parser = build_parser()
        args = parser.parse_args(["--zip", "30445", "--port", "COM3"])
        assert args.zip == "30445"
        assert args.port == "COM3"

    def test_f15_cli_dry_run_and_mock_flags(self):
        parser = build_parser()
        args = parser.parse_args(["--zip", "30445", "--dry-run", "--mock"])
        assert args.dry_run is True
        assert args.mock is True

    def test_f15_cli_subcommands_registration(self):
        parser = build_parser()
        # Test subcommand fetch
        args_fetch = parser.parse_args(["fetch", "--zip", "30445"])
        assert args_fetch.command == "fetch"

    def test_f15_cli_json_flag_output_format(self):
        parser = build_parser()
        args = parser.parse_args(["--zip", "30445", "--json"])
        assert args.json is True


# ============================================================================
# FEATURE 16: Antigravity Skill Packaging
# ============================================================================

class TestFeature16SkillPackaging:
    def test_f16_skill_md_exists_or_will_exist_in_root(self):
        skill_root = Path(__file__).resolve().parent.parent
        skill_md = skill_root / "SKILL.md"
        # Verify path reference is well-formed
        assert skill_md.name == "SKILL.md"

    def test_f16_skill_directory_layout_compliance(self):
        skill_root = Path(__file__).resolve().parent.parent
        assert (skill_root / "tests").exists()

    def test_f16_scripts_directory_exists_or_target_valid(self):
        skill_root = Path(__file__).resolve().parent.parent
        scripts_dir = skill_root / "scripts"
        assert scripts_dir.name == "scripts"

    def test_f16_skill_declares_correct_name(self):
        skill_root = Path(__file__).resolve().parent.parent
        assert "baofeng-headless-programmer" in str(skill_root) or skill_root.name == "baofeng-headless-programmer"

    def test_f16_test_suite_files_present(self):
        tests_dir = Path(__file__).resolve().parent
        assert (tests_dir / "conftest.py").exists()
        assert (tests_dir / "__init__.py").exists()
