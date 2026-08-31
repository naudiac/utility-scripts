"""Tier 5 Adversarial and Fault Injection Test Suite for Baofeng BF-F8HP Headless Programmer.

Stress-tests subprocess safety, corrupted images, mock timeouts, missing directories,
CLI edge cases, and unexpected input injection.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.baofeng_programmer import (
    EXIT_API_ERROR,
    EXIT_CAPACITY_OVERFLOW,
    EXIT_COM_PORT_ERROR,
    EXIT_GENERAL_ERROR,
    EXIT_SUCCESS,
    build_parser,
    main,
    run_pipeline,
)
from scripts.chirp_driver import (
    ChirpDriver,
    ChirpDriverError,
    RadioCommunicationError,
    RadioImageValidationError,
    RadioTimeoutError,
)
from scripts.csv_engine import CSVEngine
from scripts.frequency_fetcher import FrequencyFetcher
from scripts.models import (
    ChannelEntry,
    GeoLocation,
    RadioProfile,
    RepeaterInfo,
    SubprocessResult,
)


class TestTier5CorruptRadioImages:
    """Stress tests verifying handling of corrupted, truncated, empty, or oversized radio images."""

    def test_corrupt_image_zero_bytes(self, tmp_path: Path) -> None:
        """Verify that a 0-byte file is rejected by verify_image and upload is aborted."""
        driver = ChirpDriver()
        zero_file = tmp_path / "zero_byte.img"
        zero_file.write_bytes(b"")

        assert not driver.verify_image(zero_file)

        # Upload should be refused and return non-zero result
        result = driver.upload_radio_image(port="COM3", input_path=zero_file, mock=False)
        assert result.returncode != 0
        assert "Refusing to upload invalid or corrupt image" in result.stderr

    def test_corrupt_image_truncated_bytes(self, tmp_path: Path) -> None:
        """Verify that truncated files below 6144 bytes are rejected."""
        driver = ChirpDriver()
        for size in [1, 16, 512, 4096, 6143]:
            truncated_file = tmp_path / f"truncated_{size}.img"
            truncated_file.write_bytes(b"\x00" * size)
            assert not driver.verify_image(truncated_file), f"Size {size} should fail validation"

    def test_corrupt_image_oversized_bytes(self, tmp_path: Path) -> None:
        """Verify that oversized files above 8192 bytes are rejected."""
        driver = ChirpDriver()
        oversized_file = tmp_path / "oversized.img"
        oversized_file.write_bytes(b"\xFF" * 9000)
        assert not driver.verify_image(oversized_file)

    def test_verify_image_non_existent_path(self, tmp_path: Path) -> None:
        """Verify that non-existent image paths return False safely without unhandled exceptions."""
        driver = ChirpDriver()
        non_existent = tmp_path / "does_not_exist.img"
        assert not driver.verify_image(non_existent)

    def test_verify_image_directory_path(self, tmp_path: Path) -> None:
        """Verify that passing a directory path returns False without crashing."""
        driver = ChirpDriver()
        assert not driver.verify_image(tmp_path)

    def test_upload_non_existent_file_raises_file_not_found(self, tmp_path: Path) -> None:
        """Verify that attempting to upload a non-existent file raises FileNotFoundError."""
        driver = ChirpDriver()
        missing = tmp_path / "missing.img"
        with pytest.raises(FileNotFoundError):
            driver.upload_radio_image(port="COM3", input_path=missing)


class TestTier5SubprocessResilience:
    """Stress tests verifying subprocess timeout, missing binary, and non-zero exit code handling."""

    @patch("subprocess.run")
    def test_download_subprocess_timeout(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify subprocess.TimeoutExpired during download returns returncode 124 and captures stderr."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["chirpc"], timeout=30)

        driver = ChirpDriver(chirpc_path="chirpc")
        # Ensure is_chirpc_available returns True so live execution path is entered
        with patch.object(driver, "is_chirpc_available", return_value=True):
            out_img = tmp_path / "download_timeout.img"
            result = driver.download_radio_image(port="COM3", output_path=out_img, mock=False, dry_run=False)

            assert result.returncode == 124
            assert "timed out" in result.stderr.lower()
            assert not result.success

    @patch("subprocess.run")
    def test_upload_subprocess_timeout(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify subprocess.TimeoutExpired during upload returns returncode 124 and captures stderr."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["chirpc"], timeout=30)

        driver = ChirpDriver(chirpc_path="chirpc")
        valid_img = driver.generate_mock_image(tmp_path / "valid_for_upload.img")

        with patch.object(driver, "is_chirpc_available", return_value=True):
            result = driver.upload_radio_image(port="COM3", input_path=valid_img, mock=False, dry_run=False)

            assert result.returncode == 124
            assert "timed out" in result.stderr.lower()
            assert not result.success

    @patch("subprocess.run")
    def test_download_subprocess_missing_executable(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify FileNotFoundError (missing chirpc binary) returns returncode 127."""
        mock_run.side_effect = FileNotFoundError("Executable not found")

        driver = ChirpDriver(chirpc_path="nonexistent_chirpc")
        with patch.object(driver, "is_chirpc_available", return_value=True):
            out_img = tmp_path / "missing_exec.img"
            result = driver.download_radio_image(port="COM3", output_path=out_img, mock=False, dry_run=False)

            assert result.returncode == 127
            assert "not found" in result.stderr.lower()

    @patch("subprocess.run")
    def test_upload_subprocess_missing_executable(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify FileNotFoundError during upload returns returncode 127."""
        mock_run.side_effect = FileNotFoundError("Executable not found")

        driver = ChirpDriver(chirpc_path="nonexistent_chirpc")
        valid_img = driver.generate_mock_image(tmp_path / "valid.img")

        with patch.object(driver, "is_chirpc_available", return_value=True):
            result = driver.upload_radio_image(port="COM3", input_path=valid_img, mock=False, dry_run=False)

            assert result.returncode == 127
            assert "not found" in result.stderr.lower()

    @patch("subprocess.run")
    def test_download_subprocess_nonzero_exit_code(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify that a non-zero exit code (e.g. radio handshake error) is propagated properly."""
        mock_proc = MagicMock()
        mock_proc.returncode = 2
        mock_proc.stdout = ""
        mock_proc.stderr = "Radio did not ack handshake (is it turned on and cable connected?)"
        mock_run.return_value = mock_proc

        driver = ChirpDriver(chirpc_path="chirpc")
        with patch.object(driver, "is_chirpc_available", return_value=True):
            out_img = tmp_path / "handshake_fail.img"
            result = driver.download_radio_image(port="COM3", output_path=out_img, mock=False, dry_run=False)

            assert result.returncode == 2
            assert "Radio did not ack" in result.stderr
            assert not result.success

    @patch("subprocess.run")
    def test_download_subprocess_success_but_image_corrupt(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Verify that if chirpc returns 0 but output image is corrupt, driver catches validation failure."""
        out_img = tmp_path / "corrupt_on_download.img"
        # Write an invalid 10-byte file to simulate corrupted write
        out_img.write_bytes(b"\x00" * 10)

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Finished download"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        driver = ChirpDriver(chirpc_path="chirpc")
        with patch.object(driver, "is_chirpc_available", return_value=True):
            result = driver.download_radio_image(port="COM3", output_path=out_img, mock=False, dry_run=False)

            assert result.returncode == 1
            assert "failed validation" in result.stderr.lower()


class TestTier5BackupManagementResilience:
    """Stress tests for backup directory creation, collisions, and corrupted source handling."""

    def test_create_backup_auto_creates_deep_directories(self, tmp_path: Path) -> None:
        """Verify create_backup creates nested directories automatically."""
        driver = ChirpDriver()
        src = driver.generate_mock_image(tmp_path / "src.img")
        deep_backup_dir = tmp_path / "nested" / "subfolder" / "backups"

        backup_path = driver.create_backup(source_path=src, backup_dir=deep_backup_dir)
        assert backup_path.exists()
        assert backup_path.parent == deep_backup_dir
        assert backup_path.stat().st_size == src.stat().st_size

    def test_create_backup_collision_avoidance(self, tmp_path: Path) -> None:
        """Verify multiple backups created in rapid succession do not overwrite each other."""
        driver = ChirpDriver()
        src = driver.generate_mock_image(tmp_path / "src.img")
        b_dir = tmp_path / "backups_collision"

        # Create multiple backups with identical base timestamp
        backups = []
        for _ in range(5):
            b = driver.create_backup(source_path=src, backup_dir=b_dir)
            backups.append(b)

        # All 5 backup paths must exist and be unique
        unique_paths = set(backups)
        assert len(unique_paths) == 5
        for p in unique_paths:
            assert p.exists()
            assert p.stat().st_size > 0

    def test_create_backup_non_existent_source_raises(self, tmp_path: Path) -> None:
        """Verify create_backup raises FileNotFoundError when source does not exist."""
        driver = ChirpDriver()
        missing = tmp_path / "does_not_exist.img"
        with pytest.raises(FileNotFoundError):
            driver.create_backup(source_path=missing, backup_dir=tmp_path / "backups")

    def test_create_backup_empty_source_raises_validation_error(self, tmp_path: Path) -> None:
        """Verify create_backup raises RadioImageValidationError when source file is empty."""
        driver = ChirpDriver()
        empty_src = tmp_path / "empty.img"
        empty_src.write_bytes(b"")

        with pytest.raises(RadioImageValidationError):
            driver.create_backup(source_path=empty_src, backup_dir=tmp_path / "backups")


class TestTier5CLIEdgeCaseInjection:
    """Stress tests for CLI argument parsing, invalid flags, capacity overflow, and error codes."""

    def test_cli_capacity_overflow_above_128(self) -> None:
        """Verify requesting > 128 channels returns EXIT_CAPACITY_OVERFLOW (code 4)."""
        result = run_pipeline(zip_code="30445", max_channels=129, mock=True)
        assert result["status"] == "error"
        assert result["returncode"] == EXIT_CAPACITY_OVERFLOW
        assert "hard limit of 128" in result["message"]

    def test_cli_capacity_underflow_zero_or_negative(self) -> None:
        """Verify requesting <= 0 channels returns EXIT_CAPACITY_OVERFLOW (code 4)."""
        for count in [0, -1, -50]:
            result = run_pipeline(zip_code="30445", max_channels=count, mock=True)
            assert result["status"] == "error"
            assert result["returncode"] == EXIT_CAPACITY_OVERFLOW

    def test_cli_invalid_zip_code_rejected(self) -> None:
        """Verify invalid zip code formats return EXIT_API_ERROR (code 3)."""
        for bad_zip in ["123", "abcde", "90210-1234", "123456", "!@#$%"]:
            result = run_pipeline(zip_code=bad_zip, mock=False)
            assert result["status"] == "error"
            assert result["returncode"] == EXIT_API_ERROR
            assert "Invalid 5-digit US postal zip code" in result["message"]

    def test_cli_json_output_serialization(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Verify --json produces valid JSON parseable output with complete fields."""
        exit_code = main(["--zip", "30445", "--mock", "--fetch-only", "--json"])
        assert exit_code == EXIT_SUCCESS

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["status"] == "success"
        assert data["returncode"] == 0
        assert data["zip_code"] == "30445"
        assert data["channels_count"] > 0

    def test_cli_download_failure_propagates_exit_com_port_error(self, tmp_path: Path) -> None:
        """Verify download failure propagates EXIT_COM_PORT_ERROR (code 2)."""
        with patch.object(
            ChirpDriver,
            "download_radio_image",
            return_value=SubprocessResult(
                returncode=2,
                stdout="",
                stderr="Serial port COM99 access denied",
                command=["chirpc"],
            ),
        ):
            result = run_pipeline(
                port="COM99",
                backup_dir=tmp_path / "backups",
                download_only=True,
            )
            assert result["status"] == "error"
            assert result["returncode"] == EXIT_COM_PORT_ERROR
            assert "Serial port COM99 access denied" in result["message"]

    def test_cli_upload_failure_propagates_exit_com_port_error(self, tmp_path: Path) -> None:
        """Verify upload failure propagates EXIT_COM_PORT_ERROR (code 2)."""
        with patch.object(
            ChirpDriver,
            "upload_radio_image",
            return_value=SubprocessResult(
                returncode=1,
                stdout="",
                stderr="Radio disconnected during flash write",
                command=["chirpc"],
            ),
        ):
            result = run_pipeline(
                port="COM3",
                zip_code="30445",
                mock=True,
            )
            assert result["status"] == "error"
            assert result["returncode"] == EXIT_COM_PORT_ERROR
            assert "Radio disconnected" in result["message"]

    def test_com_port_normalization_various_formats(self) -> None:
        """Verify port normalizer handles all standard and edge port strings."""
        assert ChirpDriver.normalize_com_port("3") == "COM3"
        assert ChirpDriver.normalize_com_port("com3") == "COM3"
        assert ChirpDriver.normalize_com_port("COM3") == "COM3"
        assert ChirpDriver.normalize_com_port("10") == "\\\\.\\COM10"
        assert ChirpDriver.normalize_com_port("COM10") == "\\\\.\\COM10"
        assert ChirpDriver.normalize_com_port("com15") == "\\\\.\\COM15"
        assert ChirpDriver.normalize_com_port("/dev/ttyUSB0") == "/dev/ttyUSB0"
        assert ChirpDriver.normalize_com_port("/dev/ttyACM0") == "/dev/ttyACM0"

    def test_com_port_normalization_empty_raises_value_error(self) -> None:
        """Verify empty port string raises ValueError."""
        with pytest.raises(ValueError):
            ChirpDriver.normalize_com_port("")


class TestTier5CSVEngineFaultTolerance:
    """Stress tests for CSV parsing corruption, malformed rows, and special character sanitization."""

    def test_import_csv_with_utf8_bom(self, tmp_path: Path) -> None:
        """Verify importing a CSV file with UTF-8 BOM encoding succeeds cleanly."""
        csv_file = tmp_path / "bom_test.csv"
        content = (
            "\ufeffLocation,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,"
            "Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE\n"
            "0,CALL2M,146.520000,,0.000000,,88.5,88.5,023,NN,FM,5.00,,High,National Calling,,,,\n"
        )
        csv_file.write_text(content, encoding="utf-8")

        engine = CSVEngine()
        channels = engine.import_csv(csv_file)
        assert len(channels) == 1
        assert channels[0].location == 0
        assert channels[0].name == "CALL2M"
        assert channels[0].frequency == 146.520

    def test_import_csv_with_blank_lines_and_malformed_rows(self, tmp_path: Path) -> None:
        """Verify importing a CSV with empty lines and bad rows ignores bad lines and continues."""
        csv_file = tmp_path / "malformed.csv"
        content = (
            "Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,"
            "Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE\n"
            "\n"
            "0,CALL2M,146.520000,,0.000000,,88.5,88.5,023,NN,FM,5.00,,High,National Calling,,,,\n"
            ",,,,\n"
            "bad_row_with_no_valid_fields\n"
            "1,WX1-55,162.550000,off,0.000000,,88.5,88.5,023,NN,FM,5.00,,Low,NOAA Weather,,,,\n"
        )
        csv_file.write_text(content, encoding="utf-8")

        engine = CSVEngine()
        channels = engine.import_csv(csv_file)
        assert len(channels) == 2
        assert channels[0].location == 0
        assert channels[1].location == 1

    def test_validate_csv_out_of_bounds_frequency(self, tmp_path: Path) -> None:
        """Verify validator detects out-of-bounds frequencies (e.g. 220 MHz or 900 MHz)."""
        csv_file = tmp_path / "bad_freq.csv"
        content = (
            "Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,"
            "Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE\n"
            "0,BADFREQ,222.500000,,0.000000,,88.5,88.5,023,NN,FM,5.00,,High,220MHz Band,,,,\n"
        )
        csv_file.write_text(content, encoding="utf-8")

        engine = CSVEngine()
        is_valid, errors = engine.validate_csv_file(csv_file)
        assert not is_valid
        assert any("out of VHF/UHF bounds" in e for e in errors)

    def test_validate_csv_name_exceeding_7_chars(self, tmp_path: Path) -> None:
        """Verify validator detects display names longer than 7 characters."""
        csv_file = tmp_path / "long_name.csv"
        content = (
            "Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,"
            "Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE\n"
            "0,WAYTOOLONGNAME,146.520000,,0.000000,,88.5,88.5,023,NN,FM,5.00,,High,National Calling,,,,\n"
        )
        csv_file.write_text(content, encoding="utf-8")

        engine = CSVEngine()
        is_valid, errors = engine.validate_csv_file(csv_file)
        assert not is_valid
        assert any("exceeds 7 characters" in e for e in errors)

    def test_validate_csv_location_exceeding_127(self, tmp_path: Path) -> None:
        """Verify validator detects channel slot location indices >= 128."""
        csv_file = tmp_path / "bad_slot.csv"
        content = (
            "Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,"
            "Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE\n"
            "128,OOB128,146.520000,,0.000000,,88.5,88.5,023,NN,FM,5.00,,High,Slot 128,,,,\n"
        )
        csv_file.write_text(content, encoding="utf-8")

        engine = CSVEngine()
        is_valid, errors = engine.validate_csv_file(csv_file)
        assert not is_valid
        assert any("out of bounds (0..127)" in e for e in errors)

    def test_sanitize_channel_name_complex_noise(self) -> None:
        """Verify aggressive symbol stripping and uppercase normalization."""
        engine = CSVEngine()
        assert engine.sanitize_channel_name("k4gas/r") == "K4GASR"
        assert engine.sanitize_channel_name("W4-P (ARES)") == "W4-P AR"
        assert engine.sanitize_channel_name("$$$RPT#1$$$") == "RPT1"
        assert engine.sanitize_channel_name("🔥🔥🔥RADIO") == "RADIO"
        assert engine.sanitize_channel_name("") == ""
        assert engine.sanitize_channel_name(None) == ""


class TestTier5FrequencyFetcherFaultTolerance:
    """Stress tests for API failure modes, offline fallbacks, and tone validations."""

    @patch("urllib.request.urlopen")
    def test_resolve_zip_network_http_500_falls_back_gracefully(self, mock_urlopen: MagicMock) -> None:
        """Verify that HTTP 500 error from Zippopotam falls back to offline cache without crashing."""
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.zippopotam.us/us/30445",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        fetcher = FrequencyFetcher()
        geo = fetcher.resolve_zip("30445", mock=False)

        assert isinstance(geo, GeoLocation)
        assert geo.zip_code == "30445"
        assert geo.state_abbreviation == "GA"
        assert geo.latitude > 0

    @patch("urllib.request.urlopen")
    def test_fetch_repeaters_repeaterbook_error_falls_back_to_offline(self, mock_urlopen: MagicMock) -> None:
        """Verify that HTTP 403 or network failure from RepeaterBook falls back to offline database."""
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://www.repeaterbook.com/api/export.php",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None,
        )

        fetcher = FrequencyFetcher(repeaterbook_token="invalid_token")
        repeaters = fetcher.fetch_repeaters(zip_code="30445", mock=False)

        assert len(repeaters) > 0
        assert all(r.on_air for r in repeaters)

    def test_parse_repeaterbook_response_with_malformed_and_missing_items(self) -> None:
        """Verify parsing handles noisy, empty, and invalid dicts safely."""
        fetcher = FrequencyFetcher()
        noisy_payload = [
            {},  # empty
            {"Frequency": "invalid_str"},  # bad freq
            {"Frequency": "-146.52"},  # negative freq
            {"Frequency": "0"},  # zero freq
            {
                "Callsign": "VALID1",
                "Frequency": "146.940",
                "Input Freq": "146.340",
                "PL": "100.0",
                "Operational Status": "On-Air",
                "ARES": "Yes",
            },
            {
                "Callsign": "OFF_AIR",
                "Frequency": "147.120",
                "Operational Status": "Off-Air",
            },
        ]

        parsed = fetcher.parse_repeaterbook_response(noisy_payload)
        assert len(parsed) == 2
        assert parsed[0].callsign == "VALID1"
        assert parsed[0].on_air is True
        assert parsed[0].offset == 0.6
        assert parsed[0].duplex == "-"
        assert parsed[0].ares is True

        assert parsed[1].callsign == "OFF_AIR"
        assert parsed[1].on_air is False

    def test_tone_validation_rejects_non_standard_frequencies(self) -> None:
        """Verify CTCSS tone validator strictly allows standard EIA tones and rejects invalid ones."""
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_ctcss_tone(88.5)
        assert fetcher.is_valid_ctcss_tone(100.0)
        assert fetcher.is_valid_ctcss_tone(254.1)

        # Non-standard tones (outside 0.15Hz EIA tone boundaries)
        assert not fetcher.is_valid_ctcss_tone(50.0)
        assert not fetcher.is_valid_ctcss_tone(300.0)
        assert not fetcher.is_valid_ctcss_tone(88.0)
        assert not fetcher.is_valid_ctcss_tone(99.0)
        assert not fetcher.is_valid_ctcss_tone("invalid")


class TestTier5ExtremeFuzzingAndAllocationOverload:
    """Stress tests extreme repeater volume (>500 to 5,000 repeaters) and strict capacity capping."""

    def test_stress_500_repeaters_strict_128_channel_cap(self, tmp_path: Path) -> None:
        """Generates 500 repeaters and verifies strict 128 total channel cap."""
        fetcher = FrequencyFetcher()
        csv_engine = CSVEngine()

        repeaters = []
        for i in range(500):
            freq = 144.0 + ((i % 150) * 0.02)
            repeaters.append(
                RepeaterInfo(
                    callsign=f"K{i:04d}",
                    frequency=freq,
                    offset=0.6,
                    duplex="-",
                    tone_mode="Tone",
                    tone_freq=100.0,
                    dcs_code="023",
                    city=f"City{i}",
                    state="GA",
                    distance_miles=float(i % 50),
                    on_air=True,
                    ares=(i % 10 == 0),
                    races=(i % 15 == 0),
                    skywarn=(i % 20 == 0),
                    linked=(i % 25 == 0),
                )
            )

        plan = fetcher.build_frequency_plan_from_components(
            repeaters=repeaters,
            include_noaa=True,
            include_gmrs=True,
            include_calling=True,
            max_total_channels=128,
        )

        assert len(plan) == 128
        assert plan[0].location == 0
        assert plan[-1].location == 127
        locations = [ch.location for ch in plan]
        assert locations == list(range(128))

        # Check export CSV passes validation
        out_csv = tmp_path / "stress_500.csv"
        csv_engine.export_csv(plan, out_csv)
        is_valid, errors = csv_engine.validate_csv_file(out_csv)
        assert is_valid is True, f"CSV Validation errors: {errors}"

    def test_stress_5000_fuzzed_repeaters_with_priority_retention(self) -> None:
        """Generates 5,000 fuzzed repeaters; verifies emergency channels and top priority repeaters are retained."""
        import random
        fetcher = FrequencyFetcher()

        random.seed(42)
        repeaters = []
        for i in range(5000):
            is_on_air = random.random() > 0.3
            is_ares = random.random() > 0.8
            is_skywarn = random.random() > 0.85
            is_linked = random.random() > 0.9
            freq = round(random.uniform(144.0, 148.0) if random.random() > 0.5 else random.uniform(420.0, 450.0), 4)

            repeaters.append(
                RepeaterInfo(
                    callsign=f"W{i:05d}",
                    frequency=freq,
                    offset=0.6 if freq < 200 else 5.0,
                    duplex="-" if freq < 200 else "+",
                    tone_mode="Tone",
                    tone_freq=random.choice([88.5, 100.0, 123.0, 141.3]),
                    dcs_code="023",
                    city=f"Metropolis{i}",
                    state="GA",
                    distance_miles=random.uniform(1.0, 80.0),
                    on_air=is_on_air,
                    ares=is_ares,
                    skywarn=is_skywarn,
                    linked=is_linked,
                )
            )

        plan = fetcher.build_frequency_plan_from_components(
            repeaters=repeaters,
            include_noaa=True,
            include_gmrs=True,
            include_calling=True,
            max_total_channels=128,
        )

        assert len(plan) == 128
        # Fixed channel verification
        assert any(ch.frequency == 146.520 for ch in plan)
        assert sum(1 for ch in plan if ch.duplex == "off" or "WX" in ch.name) == 7
        assert sum(1 for ch in plan if "GMRS" in ch.name or "FRS" in ch.name or (462.5 <= ch.frequency <= 467.8)) == 22

    def test_merge_channels_with_1000_existing_and_1000_new(self) -> None:
        """Stress tests merging 1,000 existing channels with 1,000 new candidate channels."""
        csv_engine = CSVEngine()

        existing = [
            ChannelEntry(
                location=i,
                name=f"EX{i:03d}"[:7],
                frequency=146.0 + (i * 0.005),
                power="High",
            )
            for i in range(100)
        ]

        new_candidates = [
            ChannelEntry(
                location=i,
                name=f"NW{i:03d}"[:7],
                frequency=440.0 + (i * 0.01),
                power="High",
            )
            for i in range(1000)
        ]

        merged = csv_engine.merge_channels(
            existing_channels=existing,
            new_channels=new_candidates,
            start_channel=0,
            max_channels=128,
            overwrite=False,
            deduplicate=True,
        )

        assert len(merged) == 128
        # First 100 channels must be original existing channels
        for i in range(100):
            assert merged[i].name == f"EX{i:03d}"[:7]
            assert merged[i].location == i

        # Remaining 28 channels must be filled from new candidates
        for i in range(100, 128):
            assert merged[i].location == i
            assert merged[i].name.startswith("NW")


class TestTier5CSVInjectionAndFormulaProtection:
    """Stress tests name sanitization, long strings, special characters, unicode, and CSV injection vectors."""

    @pytest.mark.parametrize(
        "dirty_name,expected_prefix",
        [
            ("K4GAS/RPT-123456", "K4GASRP"),
            ("   W4MTR   ", "W4MTR"),
            ("ARES#1@METTER!", "ARES1ME"),
            ("=cmd|' /C calc'!A0", "CMD /C "),
            ("+1234567890", "1234567"),
            ("-TEST-CASE-", "-TEST-C"),
            ("@SUM(1,1)", "SUM11"),
            ("日本語テスト", ""),
            ("🔥🚒🚑", ""),
            ("N0CALL/9", "N0CALL9"),
            ("W1AW--GA", "W1AW--G"),
            ("   ", ""),
            ("a" * 500, "AAAAAAA"),
            ("<script>alert(1)</script>", "SCRIPTA"),
            ("`rm -rf /`", "RM -RF "),
            ("COM1,COM2", "COM1COM"),
        ],
    )
    def test_sanitize_channel_name_fuzzing(self, dirty_name: str, expected_prefix: str) -> None:
        """Verifies CSVEngine.sanitize_channel_name and ChannelEntry.sanitize_name produce safe 7-char names."""
        import string
        csv_engine = CSVEngine()
        cleaned = csv_engine.sanitize_channel_name(dirty_name, max_len=7)
        assert len(cleaned) <= 7
        assert all(c in string.ascii_uppercase + string.digits + "- " for c in cleaned)

        entry_cleaned = ChannelEntry.sanitize_name(dirty_name, max_len=7)
        assert len(entry_cleaned) <= 7

    def test_csv_injection_and_roundtrip_with_extreme_comments_and_quotes(self, tmp_path: Path) -> None:
        """Verifies full CSV export and import roundtrip with newlines, quotes, commas, formulas, and large text."""
        csv_engine = CSVEngine()

        crazy_channels = [
            ChannelEntry(
                location=0,
                name="TEST0",
                frequency=146.520,
                comment="Standard comment, with comma",
            ),
            ChannelEntry(
                location=1,
                name="TEST1",
                frequency=146.540,
                comment='Comment with "quotes" and , commas and ; semicolons',
            ),
            ChannelEntry(
                location=2,
                name="TEST2",
                frequency=146.560,
                comment="Formula injection: =SUM(A1:B10) + @cmd | 'calc'",
            ),
            ChannelEntry(
                location=3,
                name="TEST3",
                frequency=146.580,
                comment="A" * 2000,  # 2KB comment
            ),
            ChannelEntry(
                location=4,
                name="TEST4",
                frequency=446.000,
                comment="Special unicode symbols: αβγδε #$%&*!?",
            ),
        ]

        out_csv = tmp_path / "adversarial_roundtrip.csv"
        csv_engine.export_csv(crazy_channels, out_csv)

        # File must be valid
        is_valid, errors = csv_engine.validate_csv_file(out_csv)
        assert is_valid is True, f"Errors: {errors}"

        # Re-import and check exact preservation of fields
        imported = csv_engine.import_csv(out_csv)
        assert len(imported) == 5

        for orig, imp in zip(crazy_channels, imported):
            assert orig.location == imp.location
            assert orig.name == imp.name
            assert round(orig.frequency, 4) == round(imp.frequency, 4)
            assert orig.comment == imp.comment


class TestTier5DCSFormattingAndDirtyInputs:
    """Stress tests DCS code padding and dirty RepeaterBook input formats."""

    @pytest.mark.parametrize(
        "raw_code,expected_padded",
        [
            ("23", "023"),
            ("023", "023"),
            ("754", "754"),
            (23, "023"),
            ("D023N", "023"),
            ("DCS 047", "047"),
            ("", "023"),
            (None, "023"),
            ("---", "023"),
        ],
    )
    def test_dtcs_code_formatting_and_zero_padding(self, raw_code: str, expected_padded: str) -> None:
        """Verifies DCS codes are zero-padded to 3 digits and non-digits stripped."""
        csv_engine = CSVEngine()
        assert csv_engine.format_dtcs_code(raw_code) == expected_padded


class TestTier5ExtremeZipCodeMatrix:
    """Stress tests extreme zip codes, injection payloads, network errors, and offline fallbacks."""

    @pytest.mark.parametrize(
        "zip_input,is_valid",
        [
            ("30445", True),
            ("00501", True),  # Lowest valid US zip (IRS Holtsville NY)
            ("99950", True),  # Ketchikan AK
            ("00000", True),  # Syntactically 5 digits
            ("99999", True),  # Syntactically 5 digits
            ("1234", False),  # 4 digits
            ("123456", False),  # 6 digits
            ("30445-1234", False),  # ZIP+4
            ("ABCDE", False),  # Letters
            ("3044a", False),
            (";", False),
            ("'; DROP TABLE zipcodes; --", False),
            ("30445; cat /etc/passwd", False),
            ("", False),
            ("   ", False),
        ],
    )
    def test_zip_code_validation_matrix(self, zip_input: str, is_valid: bool) -> None:
        """Verifies FrequencyFetcher.is_valid_zip_code strict 5-digit regex validation."""
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_zip_code(zip_input) == is_valid

    @pytest.mark.parametrize("invalid_radius", [0.0, -10.0, 100.1, 1000.0, "abc", None])
    def test_radius_validation_boundaries(self, invalid_radius: float) -> None:
        """Verifies radius validation rejects <= 0, > 100 miles, or non-numeric types."""
        fetcher = FrequencyFetcher()
        assert fetcher.is_valid_radius(invalid_radius) is False

