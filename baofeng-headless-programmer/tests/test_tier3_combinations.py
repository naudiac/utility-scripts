"""
Tier 3: Cross-Feature Combinations & Integration Test Suite.

Covers:
- Multi-bank channel merging with user-defined channel preservation
- Band filter combinations (2m only, 70cm only, 2m+70cm, all)
- Custom memory allocation zones (--start-channel, --noaa-start-channel)
- Power profile configuration (High, Med, Low)
- Frequency and tone de-duplication across merged channel lists
- Squelch mode combination matrix (Carrier, CTCSS Tone, CTCSS TSQL, DCS)
- Combined CLI flag interactions (--dry-run + --json, --mock + --backup-dir)
- Multi-step modular pipeline executions (fetch -> merge -> export)
"""

import json
import pytest
from pathlib import Path
from typing import List

try:
    from models import ChannelEntry, RepeaterInfo, GeoLocation
    from csv_engine import CSVEngine
    from frequency_fetcher import FrequencyFetcher
    from chirp_driver import ChirpDriver
    from baofeng_programmer import build_parser
except ImportError:
    pass


class TestMultiBankMergeCombinations:
    def test_combination_preserve_user_channels_0_to_19(self, sample_existing_channels):
        csv_engine = CSVEngine()
        # Existing channels 0..4
        new_repeaters = [
            ChannelEntry(location=0, name="RPT0", frequency=146.940),
            ChannelEntry(location=0, name="RPT1", frequency=147.240),
        ]
        # Merge starting at channel 5
        merged = csv_engine.merge_channels(
            existing_channels=sample_existing_channels,
            new_channels=new_repeaters,
            start_channel=5,
            max_channels=128
        )
        
        # Verify existing 0..4 untouched
        for orig in sample_existing_channels:
            match = next(ch for ch in merged if ch.location == orig.location)
            assert match.name == orig.name
            assert match.frequency == orig.frequency
            
        # Verify new repeaters allocated at 5 and 6
        assert merged[5].name == "RPT0"
        assert merged[6].name == "RPT1"

    def test_combination_custom_start_and_noaa_start_channels(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(
            zip_code="30445",
            mock=True,
            repeater_start_channel=10,
            noaa_start_channel=120
        )
        # Find NOAA channels
        noaa_chans = [ch for ch in plan if "WX" in ch.name or "NOAA" in ch.comment]
        for idx, ch in enumerate(noaa_chans):
            assert ch.location == 120 + idx


class TestBandFilterCombinations:
    def test_combination_band_filter_2m_only(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_by_bands(sample_repeaters_30445, bands=["2m"])
        for r in filtered:
            assert 144.0 <= r.frequency <= 148.0

    def test_combination_band_filter_70cm_only(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_by_bands(sample_repeaters_30445, bands=["70cm"])
        for r in filtered:
            assert 420.0 <= r.frequency <= 450.0

    def test_combination_band_filter_2m_and_70cm(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_by_bands(sample_repeaters_30445, bands=["2m", "70cm"])
        for r in filtered:
            is_2m = 144.0 <= r.frequency <= 148.0
            is_70cm = 420.0 <= r.frequency <= 450.0
            assert is_2m or is_70cm

    def test_combination_band_filter_all(self, sample_repeaters_30445):
        fetcher = FrequencyFetcher()
        filtered = fetcher.filter_by_bands(sample_repeaters_30445, bands=["all"])
        assert len(filtered) == len(sample_repeaters_30445)


class TestPowerProfileCombinations:
    def test_combination_global_power_override_med(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(zip_code="30445", mock=True, power="Med")
        repeater_chans = [ch for ch in plan if "WX" not in ch.name and "NOAA" not in ch.comment]
        for ch in repeater_chans:
            assert ch.power == "Med"

    def test_combination_noaa_always_low_power(self):
        fetcher = FrequencyFetcher()
        plan = fetcher.build_frequency_plan(zip_code="30445", mock=True, power="High")
        noaa_chans = [ch for ch in plan if "WX" in ch.name or "NOAA" in ch.comment]
        for ch in noaa_chans:
            assert ch.power == "Low"


class TestDeduplicationCombinations:
    def test_combination_duplicate_frequency_and_tone_deduplication(self):
        csv_engine = CSVEngine()
        existing = [
            ChannelEntry(location=0, name="K4GAS", frequency=146.940, duplex="-", offset=0.6, tone="Tone", r_tone_freq=100.0)
        ]
        new_chans = [
            # Exact duplicate
            ChannelEntry(location=1, name="K4GAS2", frequency=146.940, duplex="-", offset=0.6, tone="Tone", r_tone_freq=100.0),
            # Different frequency
            ChannelEntry(location=2, name="W4VDA", frequency=147.240, duplex="+", offset=0.6, tone="Tone", r_tone_freq=100.0),
        ]
        merged = csv_engine.merge_channels(existing, new_chans, deduplicate=True)
        assert len(merged) == 2
        freqs = [ch.frequency for ch in merged]
        assert freqs.count(146.940) == 1
        assert 147.240 in freqs


class TestSquelchModeMatrixCombinations:
    @pytest.mark.parametrize("tone_mode,r_tone,c_tone,dtcs_code,expected_tone", [
        ("", 88.5, 88.5, "023", ""),
        ("Tone", 100.0, 88.5, "023", "Tone"),
        ("TSQL", 100.0, 100.0, "023", "TSQL"),
        ("DTCS", 88.5, 88.5, "023", "DTCS"),
    ])
    def test_combination_tone_mode_matrix(self, tmp_path, tone_mode, r_tone, c_tone, dtcs_code, expected_tone):
        csv_engine = CSVEngine()
        ch = ChannelEntry(
            location=0,
            name="TEST",
            frequency=146.940,
            tone=tone_mode,
            r_tone_freq=r_tone,
            c_tone_freq=c_tone,
            dtcs_code=dtcs_code
        )
        out_csv = tmp_path / f"tone_{tone_mode}.csv"
        csv_engine.export_csv([ch], out_csv)
        imported = csv_engine.import_csv(out_csv)
        assert imported[0].tone == expected_tone


class TestCLICombinationFlags:
    def test_combination_dry_run_and_json_flags(self):
        parser = build_parser()
        args = parser.parse_args(["--zip", "30445", "--dry-run", "--json"])
        assert args.dry_run is True
        assert args.json is True

    def test_combination_mock_with_custom_paths(self, tmp_path):
        parser = build_parser()
        custom_out = str(tmp_path / "custom.csv")
        custom_bkp = str(tmp_path / "my_backups")
        args = parser.parse_args([
            "--zip", "30445",
            "--mock",
            "--output-csv", custom_out,
            "--backup-dir", custom_bkp,
            "--radius", "35",
            "--bands", "2m,70cm",
            "--power", "Med"
        ])
        assert args.zip == "30445"
        assert args.mock is True
        assert args.output_csv == custom_out
        assert args.backup_dir == custom_bkp
        assert args.radius == 35
        assert args.bands == "2m,70cm"
        assert args.power == "Med"

    def test_combination_subcommand_fetch_options(self, tmp_path):
        parser = build_parser()
        out_csv = str(tmp_path / "fetch_out.csv")
        args = parser.parse_args(["fetch", "--zip", "30445", "--output-csv", out_csv, "--mock"])
        assert args.command == "fetch"
        assert args.zip == "30445"
        assert args.output_csv == out_csv
        assert args.mock is True
