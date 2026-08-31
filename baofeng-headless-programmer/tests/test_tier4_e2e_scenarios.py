"""
Tier 4: Realistic End-to-End Scenarios Test Suite.

Covers the 5 core real-world application scenarios defined in TEST_INFRA.md:
1. Scenario 1: Standard Metter, GA Deployment (Zip 30445 Acceptance Test)
2. Scenario 2: Dense Metro Area Plan (Max Channel Capping & EmComm Prioritization)
3. Scenario 3: Minimal Rural Area (Sparse Repeaters & Baseline Protection)
4. Scenario 4: Offline Disaster Recovery Mode (Zero Network Fallback)
5. Scenario 5: Custom Channel Offset & Power Profile (Preserving User Channels 0-19)
"""

import os
import json
import pytest
from pathlib import Path
from typing import List

try:
    from models import ChannelEntry, RepeaterInfo, GeoLocation
    from chirp_driver import ChirpDriver
    from frequency_fetcher import FrequencyFetcher
    from csv_engine import CSVEngine
    from baofeng_programmer import run_pipeline, build_parser
except ImportError:
    pass


class TestScenario1StandardMetterGADeployment:
    """
    Scenario 1: Standard Metter, GA Deployment (Zip 30445 Acceptance Test)
    Verifies AC-1, AC-2, AC-3, AC-4 from ORIGINAL_REQUEST.md.
    """
    def test_scenario_1_full_pipeline_mock_zip_30445(self, tmp_path):
        out_csv = tmp_path / "output_30445.csv"
        backup_dir = tmp_path / "backups_30445"
        
        # Execute pipeline
        result = run_pipeline(
            zip_code="30445",
            port="COM3",
            dry_run=True,
            mock=True,
            output_csv=out_csv,
            backup_dir=backup_dir,
            radio_model="Baofeng_BF-F8HP"
        )
        
        # 1. Pipeline returns success status code 0
        assert result.get("status") == "success"
        
        # 2. Output CSV exists
        assert out_csv.exists()
        
        # 3. Read and inspect CSV entries
        csv_engine = CSVEngine()
        channels = csv_engine.import_csv(out_csv)
        assert len(channels) >= 30  # NOAA(7) + GMRS(22) + Simplex(1) + Repeaters(>=3)
        
        # AC-1: Contains >= 3 amateur repeaters
        repeater_chans = [
            ch for ch in channels
            if "WX" not in ch.name and "GMRS" not in ch.name and round(ch.frequency, 4) != 146.5200
        ]
        assert len(repeater_chans) >= 3
        
        # AC-2: Contains all 7 NOAA weather frequencies
        noaa_freqs = {162.400, 162.425, 162.450, 162.475, 162.500, 162.525, 162.550}
        actual_noaa = {round(ch.frequency, 4) for ch in channels if "WX" in ch.name or "NOAA" in ch.comment}
        assert actual_noaa == noaa_freqs
        
        # National VHF Calling frequency injected (146.520)
        assert any(round(ch.frequency, 4) == 146.5200 for ch in channels)
        
        # GMRS/FRS channels 1-22 injected
        gmrs_chans = [ch for ch in channels if "GMRS" in ch.name or "FRS" in ch.name or (462.5 <= ch.frequency <= 467.8)]
        assert len(gmrs_chans) >= 22
        
        # AC-3: Valid 19-column CHIRP format
        is_valid, errors = csv_engine.validate_csv_file(out_csv)
        assert is_valid is True, f"CSV validation errors: {errors}"
        
        # AC-4: Backups created
        backup_files = list(backup_dir.glob("backup_*"))
        assert len(backup_files) >= 1
        assert any(f.suffix == ".img" for f in backup_files)


class TestScenario2DenseMetroAreaPlan:
    """
    Scenario 2: Dense Metro Area Plan (Max Channel Capping & EmComm Prioritization)
    Verifies handling >150 repeaters, strict On-Air filtering, ARES/Linked ranking, exactly 128 channels.
    """
    def test_scenario_2_dense_metro_150_repeaters_capped_at_128(self, tmp_path):
        fetcher = FrequencyFetcher()
        csv_engine = CSVEngine()
        
        # Create 160 synthetic repeaters (some off-air, some ARES/Linked)
        synthetic_repeaters = []
        for i in range(160):
            is_on_air = (i % 5 != 0)  # 20% off-air
            is_ares = (i % 3 == 0)
            is_linked = (i % 4 == 0)
            is_skywarn = (i % 6 == 0)
            freq = 145.0 + (i * 0.02)
            if freq > 148.0:
                freq = 440.0 + ((i - 150) * 0.05)
            synthetic_repeaters.append(
                RepeaterInfo(
                    callsign=f"RPT{i:03d}",
                    frequency=freq,
                    offset=0.6 if freq < 200 else 5.0,
                    duplex="-" if i % 2 == 0 else "+",
                    tone_mode="Tone",
                    tone_freq=100.0,
                    dcs_code="023",
                    city="MetroCity",
                    state="GA",
                    distance_miles=float(i % 35),
                    on_air=is_on_air,
                    ares=is_ares,
                    races=False,
                    skywarn=is_skywarn,
                    linked=is_linked
                )
            )
        
        # Filter & prioritize
        filtered = fetcher.filter_on_air(synthetic_repeaters)
        prioritized = fetcher.prioritize_repeaters(filtered)
        
        # Top items should have emergency flags
        assert prioritized[0].ares or prioritized[0].linked or prioritized[0].skywarn
        
        # Build complete plan
        plan = fetcher.build_frequency_plan_from_components(
            repeaters=prioritized,
            include_noaa=True,
            include_gmrs=True,
            include_calling=True,
            max_total_channels=128
        )
        
        assert len(plan) == 128
        assert plan[-1].location == 127
        
        # Verify CSV export and compliance
        out_csv = tmp_path / "metro_128.csv"
        csv_engine.export_csv(plan, out_csv)
        is_valid, errors = csv_engine.validate_csv_file(out_csv)
        assert is_valid is True


class TestScenario3MinimalRuralArea:
    """
    Scenario 3: Minimal Rural Area (Sparse Repeaters & Baseline Protection)
    Verifies graceful handling when only 1-2 repeaters are available.
    """
    def test_scenario_3_sparse_rural_area(self, tmp_path):
        fetcher = FrequencyFetcher()
        csv_engine = CSVEngine()
        
        # Only 2 repeaters available in rural county
        rural_repeaters = [
            RepeaterInfo("K4RUR", 146.820, 0.6, "-", "Tone", 100.0, "023", "Rural", "GA", 12.0, on_air=True),
            RepeaterInfo("W4CTY", 443.200, 5.0, "+", "Tone", 123.0, "023", "County", "GA", 18.0, on_air=True),
        ]
        
        plan = fetcher.build_frequency_plan_from_components(
            repeaters=rural_repeaters,
            include_noaa=True,
            include_gmrs=True,
            include_calling=True,
            max_total_channels=128
        )
        
        # 1 calling + 2 repeaters + 22 GMRS + 7 NOAA = 32 channels
        assert len(plan) == 32
        
        out_csv = tmp_path / "rural.csv"
        csv_engine.export_csv(plan, out_csv)
        assert out_csv.exists()
        
        # Verify all 32 channels are unique and properly indexed
        locations = [ch.location for ch in plan]
        assert len(locations) == len(set(locations))


class TestScenario4OfflineDisasterRecoveryMode:
    """
    Scenario 4: Offline Disaster Recovery Mode (Zero Network Fallback)
    Simulates complete offline operation with fallback dataset.
    """
    def test_scenario_4_offline_disaster_recovery(self, tmp_path):
        out_csv = tmp_path / "disaster_recovery.csv"
        backup_dir = tmp_path / "disaster_backups"
        
        result = run_pipeline(
            zip_code="30445",
            port="COM4",
            dry_run=True,
            mock=True,
            output_csv=out_csv,
            backup_dir=backup_dir
        )
        
        assert result.get("status") == "success"
        assert out_csv.exists()
        
        # Ensure NOAA channels are configured with TX-Inhibit (safety in disaster)
        csv_engine = CSVEngine()
        channels = csv_engine.import_csv(out_csv)
        noaa_chans = [ch for ch in channels if "WX" in ch.name or "NOAA" in ch.comment]
        for ch in noaa_chans:
            assert ch.duplex in ["", "off"]
            assert ch.power == "Low"


class TestScenario5CustomChannelOffsetAndPowerProfile:
    """
    Scenario 5: Custom Channel Offset & Power Profile (Preserving User Channels 0-19)
    Verifies user channels 0-19 are preserved, repeaters start at 20, NOAA at 120.
    """
    def test_scenario_5_preserve_user_channels_and_custom_offsets(self, tmp_path, sample_existing_channels):
        csv_engine = CSVEngine()
        fetcher = FrequencyFetcher()
        
        # Build 10 new repeaters
        repeaters = [
            RepeaterInfo(f"RPT{i}", 146.60 + (i*0.02), 0.6, "-", "Tone", 100.0, "023", "City", "GA", 5.0, on_air=True)
            for i in range(10)
        ]
        
        new_plan = fetcher.build_frequency_plan_from_components(
            repeaters=repeaters,
            include_noaa=True,
            include_gmrs=False,
            include_calling=False,
            repeater_start_channel=20,
            noaa_start_channel=120
        )
        
        # Merge with existing channels 0..4
        merged = csv_engine.merge_channels(
            existing_channels=sample_existing_channels,
            new_channels=new_plan,
            max_channels=128
        )
        
        # 1. Existing channels 0..4 intact
        for orig in sample_existing_channels:
            match = next(ch for ch in merged if ch.location == orig.location)
            assert match.name == orig.name
            assert match.frequency == orig.frequency
            
        # 2. Repeaters start at channel 20
        repeater_merged = [ch for ch in merged if 20 <= ch.location < 30]
        assert len(repeater_merged) == 10
        assert repeater_merged[0].location == 20
        
        # 3. NOAA placed at 120..126
        noaa_merged = [ch for ch in merged if 120 <= ch.location <= 126]
        assert len(noaa_merged) == 7
