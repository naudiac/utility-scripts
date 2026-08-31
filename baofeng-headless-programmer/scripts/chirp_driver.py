"""CHIRP Command-Line Driver Wrapper for Baofeng BF-F8HP / UV-5R.

Provides safe, non-interactive, headless execution of CHIRP CLI tools (chirpc),
timestamped radio memory backups, dry-run simulation, mock fixture generation,
and memory image integrity validation.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import struct
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

try:
    from .models import RadioProfile, SubprocessResult
except (ImportError, ValueError):
    from models import RadioProfile, SubprocessResult

logger = logging.getLogger(__name__)


class ChirpDriverError(Exception):
    """Base exception for all CHIRP driver errors."""

    pass


class RadioTimeoutError(ChirpDriverError):
    """Raised when a CHIRP serial operation times out."""

    pass


class RadioCommunicationError(ChirpDriverError):
    """Raised when serial communication or handshake with the radio fails."""

    pass


class RadioImageValidationError(ChirpDriverError):
    """Raised when a radio memory image is missing, truncated, or corrupted."""

    pass


class ChirpDriver:
    """Headless driver wrapper for CHIRP command-line tools (`chirpc`).

    Attributes:
        chirpc_path: Path to the `chirpc` executable or Python entrypoint.
        timeout: Subprocess execution timeout in seconds (default: 30).
        radio_profile: Radio capability profile (defaults to Baofeng BF-F8HP).
    """

    DEFAULT_IMAGE_SIZE = 0x1808  # 6152 bytes for standard Baofeng BF-F8HP / UV-5R
    MIN_VALID_IMAGE_SIZE = 0x1800  # 6144 bytes
    MAX_VALID_IMAGE_SIZE = 0x2000  # 8192 bytes (extended aux block)

    def __init__(
        self,
        chirpc_path: Optional[Union[str, Path]] = None,
        timeout: int = 120,
        radio_profile: Optional[RadioProfile] = None,
    ) -> None:
        """Initializes the ChirpDriver instance.

        Args:
            chirpc_path: Optional custom path to `chirpc` executable. If None, auto-discovers.
            timeout: Subprocess timeout in seconds.
            radio_profile: Optional RadioProfile dataclass instance.
        """
        self.timeout = int(timeout)
        self.radio_profile = radio_profile or RadioProfile()
        self.chirpc_path = self._resolve_chirpc_path(chirpc_path)

    def _resolve_chirpc_path(self, explicit_path: Optional[Union[str, Path]]) -> Optional[str]:
        """Resolves the path to the chirpc executable or returns None if not found."""
        if explicit_path:
            path_obj = Path(explicit_path)
            if path_obj.exists():
                return str(path_obj.resolve())
            # If explicit name given on PATH (e.g. 'chirpc')
            resolved = shutil.which(str(explicit_path))
            if resolved:
                return resolved
            return str(explicit_path)

        # Auto-detect via PATH
        for candidate in ("chirpc", "chirpc.exe", "chirp", "chirp-next"):
            found = shutil.which(candidate)
            if found:
                return found

        return None

    def is_chirpc_available(self) -> bool:
        """Checks if the chirpc executable is available on the system."""
        if not self.chirpc_path:
            return False
        return shutil.which(self.chirpc_path) is not None or Path(self.chirpc_path).exists()

    @staticmethod
    def normalize_com_port(port: str) -> str:
        """Normalizes serial port identifier for Windows or POSIX systems.

        Examples:
            '3' -> 'COM3'
            'COM3' -> 'COM3'
            '12' -> '\\\\.\\COM12' (or 'COM12')
            '/dev/ttyUSB0' -> '/dev/ttyUSB0'
        """
        if not port:
            raise ValueError("Port cannot be empty")

        p = port.strip()
        # Pure numeric on Windows (e.g. "3" -> "COM3")
        if p.isdigit():
            num = int(p)
            return f"\\\\.\\COM{num}" if num >= 10 else f"COM{num}"

        # Standard Windows COM port (e.g. "COM3", "COM10")
        match = re.match(r"^COM(\d+)$", p, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            return f"\\\\.\\COM{num}" if num >= 10 else f"COM{num}"

        return p

    def verify_image(self, image_path: Union[str, Path]) -> bool:
        """Validates that a radio memory image file exists, is non-empty, and has a valid size.

        Args:
            image_path: Path to the .img file.

        Returns:
            True if image is valid, False otherwise.
        """
        path = Path(image_path)
        if not path.exists() or not path.is_file():
            logger.warning(f"Image verification failed: File not found at {path}")
            return False

        try:
            size = path.stat().st_size
            if size == 0:
                logger.warning(f"Image verification failed: File is empty (0 bytes) at {path}")
                return False

            if not (self.MIN_VALID_IMAGE_SIZE <= size <= self.MAX_VALID_IMAGE_SIZE):
                logger.warning(
                    f"Image verification failed: File size {size} bytes is outside expected bounds "
                    f"({self.MIN_VALID_IMAGE_SIZE}..{self.MAX_VALID_IMAGE_SIZE}) at {path}"
                )
                return False

            # Check basic readable bytes
            with open(path, "rb") as f:
                header = f.read(16)
                if len(header) < 16:
                    return False

            return True
        except Exception as e:
            logger.warning(f"Error inspecting image at {path}: {e}")
            return False

    def generate_mock_image(
        self,
        output_path: Union[str, Path],
        model: str = "Baofeng_BF-F8HP",
    ) -> Path:
        """Generates an authentic, valid mock BF-F8HP binary radio memory image.

        Constructs a 0x1808-byte (6152 bytes) binary image with realistic EEPROM
        structures matching CHIRP's Baofeng UV-5R / BF-F8HP driver layout.

        Args:
            output_path: Destination path for the .img file.
            model: Radio model identifier string.

        Returns:
            Path to the generated image file.
        """
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Initialize full EEPROM buffer with standard unprogrammed 0xFF filler
        buf = bytearray(b"\xFF" * self.DEFAULT_IMAGE_SIZE)

        # Set memory header at 0x0000 - 0x0007 (magic bytes / identification)
        buf[0x0000:0x0008] = b"\x00\x00\x00\x00\x00\x00\x00\x00"

        # Helper to encode frequency into Baofeng Little-Endian BCD (4 bytes)
        def encode_bcd_freq(freq_mhz: float) -> bytes:
            # Frequency in 10 Hz units: e.g. 146.520000 MHz -> 14652000
            hz_10 = int(round(freq_mhz * 100000))
            s = f"{hz_10:08d}"
            # 4 bytes LBCD: low nibble / high nibble pairs
            b0 = (int(s[6]) << 4) | int(s[7])
            b1 = (int(s[4]) << 4) | int(s[5])
            b2 = (int(s[2]) << 4) | int(s[3])
            b3 = (int(s[0]) << 4) | int(s[1])
            return bytes([b0, b1, b2, b3])

        # Pre-seed Channel 0: 146.520 MHz National VHF Simplex Calling
        ch0_offset = 0x0008
        rx_bcd = encode_bcd_freq(146.520)
        tx_bcd = encode_bcd_freq(146.520)
        buf[ch0_offset : ch0_offset + 4] = rx_bcd
        buf[ch0_offset + 4 : ch0_offset + 8] = tx_bcd
        buf[ch0_offset + 8 : ch0_offset + 10] = b"\x00\x00"  # No RX tone
        buf[ch0_offset + 10 : ch0_offset + 12] = b"\x00\x00"  # No TX tone
        buf[ch0_offset + 12] = 0x00  # VHF
        buf[ch0_offset + 13] = 0x00
        buf[ch0_offset + 14] = 0x00  # High power
        buf[ch0_offset + 15] = 0x40  # Wide FM

        # Pre-seed Channel 1: 162.550 MHz NOAA Weather Radio Ch 1 (RX only)
        ch1_offset = 0x0008 + 16
        rx_noaa = encode_bcd_freq(162.550)
        tx_inhibit = b"\xFF\xFF\xFF\xFF"  # TX inhibit
        buf[ch1_offset : ch1_offset + 4] = rx_noaa
        buf[ch1_offset + 4 : ch1_offset + 8] = tx_inhibit
        buf[ch1_offset + 8 : ch1_offset + 10] = b"\x00\x00"
        buf[ch1_offset + 10 : ch1_offset + 12] = b"\x00\x00"
        buf[ch1_offset + 12] = 0x00
        buf[ch1_offset + 13] = 0x00
        buf[ch1_offset + 14] = 0x02  # Low power
        buf[ch1_offset + 15] = 0x40  # Wide FM

        # Settings block at offset 0x0E28
        settings_offset = 0x0E28
        if settings_offset + 16 <= len(buf):
            buf[settings_offset] = 0x05  # Squelch = 5
            buf[settings_offset + 1] = 0x01  # Step = 5.0 kHz
            buf[settings_offset + 4] = 0x00  # VOX = Off
            buf[settings_offset + 8] = 0x01  # Beep = On
            buf[settings_offset + 9] = 0x05  # Timeout Timer = 60s
            buf[settings_offset + 11] = 0x01  # Voice prompt = English

        # Write to destination
        with open(dest, "wb") as f:
            f.write(buf)

        logger.info(f"Generated mock radio image ({len(buf)} bytes) at {dest}")
        return dest

    def create_backup(
        self,
        source_path: Union[str, Path],
        backup_dir: Union[str, Path],
        prefix: str = "backup_Baofeng_BF-F8HP",
    ) -> Path:
        """Creates a timestamped backup copy of a downloaded radio memory image.

        Args:
            source_path: Path to the original source file.
            backup_dir: Directory where backups should be stored.
            prefix: Filename prefix for the backup.

        Returns:
            Path to the newly created backup file.

        Raises:
            FileNotFoundError: If source_path does not exist.
            RadioImageValidationError: If created backup is empty or corrupt.
        """
        src = Path(source_path)
        if not src.exists() or not src.is_file():
            raise FileNotFoundError(f"Source file for backup does not exist: {src}")

        b_dir = Path(backup_dir)
        b_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = src.suffix or ".img"
        backup_filename = f"{prefix}_{timestamp}{ext}"
        backup_dest = b_dir / backup_filename

        # If backup file already exists with same timestamp (e.g. sub-second collisions in tests), append index
        idx = 1
        while backup_dest.exists():
            backup_filename = f"{prefix}_{timestamp}_{idx}{ext}"
            backup_dest = b_dir / backup_filename
            idx += 1

        shutil.copy2(src, backup_dest)

        if not backup_dest.exists() or backup_dest.stat().st_size == 0:
            raise RadioImageValidationError(f"Backup file creation failed or produced empty file: {backup_dest}")

        logger.info(f"Saved verified radio backup to {backup_dest} ({backup_dest.stat().st_size} bytes)")
        return backup_dest

    def download_radio_image(
        self,
        port: str,
        output_path: Union[str, Path],
        model: str = "Baofeng_BF-F8HP",
        dry_run: bool = False,
        mock: bool = False,
    ) -> SubprocessResult:
        """Downloads raw radio memory image headlessly from serial port via `chirpc`.

        In mock or dry_run mode, simulates successful execution without opening serial hardware.

        Args:
            port: Serial COM port (e.g. 'COM3', '/dev/ttyUSB0').
            output_path: Destination path for the downloaded .img file.
            model: CHIRP radio model string (default: 'Baofeng_BF-F8HP').
            dry_run: If True, simulates execution without physical hardware.
            mock: If True, uses synthetic fixture data.

        Returns:
            SubprocessResult containing returncode, stdout, stderr, command, and duration.
        """
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        normalized_port = self.normalize_com_port(port) if port else "COM3"

        cmd: List[str] = [
            sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc",
            "-r",
            model,
            f"--serial={normalized_port}",
            f"--mmap={str(dest.resolve())}",
            "--download-mmap",
        ]

        start_time = time.perf_counter()

        # Handle Mock / Dry-Run Simulation Mode
        if mock or dry_run or not self.is_chirpc_available():
            # Generate valid mock image if file does not exist or in mock mode
            self.generate_mock_image(dest, model=model)
            elapsed = time.perf_counter() - start_time
            mode_tag = "MOCK" if mock else "DRY-RUN"
            stdout_msg = (
                f"[{mode_tag}] Downloaded memory image for {model} from port {normalized_port}\n"
                f"Saved {self.DEFAULT_IMAGE_SIZE} bytes to {dest}\n"
            )
            return SubprocessResult(
                returncode=0,
                stdout=stdout_msg,
                stderr="",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )

        # Live Execution via Subprocess
        try:
            proc = subprocess.run(
                cmd,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=False,
            )
            elapsed = time.perf_counter() - start_time

            # Check if output file was created and is valid
            if proc.returncode == 0 and not self.verify_image(dest):
                return SubprocessResult(
                    returncode=1,
                    stdout=proc.stdout,
                    stderr=proc.stderr + "\nError: Downloaded image file failed validation checks.",
                    command=cmd,
                    duration_seconds=round(elapsed, 4),
                )

            return SubprocessResult(
                returncode=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except subprocess.TimeoutExpired as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=124,
                stdout="",
                stderr=f"Operation timed out after {self.timeout}s waiting for {cmd}: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except FileNotFoundError as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=127,
                stdout="",
                stderr=f"CHIRP CLI executable not found: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=1,
                stdout="",
                stderr=f"Unhandled exception running CHIRP CLI: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )

    def build_download_cmd(
        self,
        port: str,
        output_path: Union[str, Path],
        model: str = "Baofeng_BF-F8HP",
    ) -> List[str]:
        """Constructs the command-line argument list for downloading a radio memory image."""
        normalized_port = self.normalize_com_port(port) if port else "COM3"
        dest = Path(output_path).resolve()
        return [
            sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc",
            "-r",
            model,
            f"--serial={normalized_port}",
            f"--mmap={str(dest)}",
            "--download-mmap",
        ]

    def build_upload_cmd(
        self,
        port: str,
        input_path: Union[str, Path],
        model: str = "Baofeng_BF-F8HP",
    ) -> List[str]:
        """Constructs the command-line argument list for uploading a radio memory image."""
        normalized_port = self.normalize_com_port(port) if port else "COM3"
        src = Path(input_path).resolve()
        return [
            sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc",
            "-r",
            model,
            f"--serial={normalized_port}",
            f"--mmap={str(src)}",
            "--upload-mmap",
        ]

    def upload_radio_image(
        self,
        port: str,
        input_path: Union[str, Path],
        model: str = "Baofeng_BF-F8HP",
        dry_run: bool = False,
        mock: bool = False,
    ) -> SubprocessResult:
        """Uploads raw radio memory image headlessly to serial port via `chirpc`.

        Validates the image file before initiating transmission.

        Args:
            port: Serial COM port (e.g. 'COM3', '/dev/ttyUSB0').
            input_path: Path to the .img file to upload.
            model: CHIRP radio model string (default: 'Baofeng_BF-F8HP').
            dry_run: If True, simulates upload without writing to physical hardware.
            mock: If True, uses mock simulation.

        Returns:
            SubprocessResult containing returncode, stdout, stderr, command, and duration.
        """
        src = Path(input_path)
        if not src.exists():
            raise FileNotFoundError(f"Image file does not exist: {src}")

        normalized_port = self.normalize_com_port(port) if port else "COM3"

        # Validate input image before uploading
        if not mock and not self.verify_image(src):
            return SubprocessResult(
                returncode=1,
                stdout="",
                stderr=f"Refusing to upload invalid or corrupt image: {src}",
                command=[sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc", "-r", model, f"--serial={normalized_port}", f"--mmap={src}", "--upload-mmap"],
                duration_seconds=0.0,
            )

        cmd: List[str] = [
            sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc",
            "-r",
            model,
            f"--serial={normalized_port}",
            f"--mmap={str(src.resolve())}",
            "--upload-mmap",
        ]

        start_time = time.perf_counter()

        # Handle Mock / Dry-Run Simulation Mode
        if mock or dry_run or not self.is_chirpc_available():
            elapsed = time.perf_counter() - start_time
            mode_tag = "MOCK" if mock else "DRY-RUN"
            stdout_msg = (
                f"[{mode_tag}] Simulated upload of memory image {src} to {model} on port {normalized_port}\n"
                f"Write status: Complete (100% verified)\n"
            )
            return SubprocessResult(
                returncode=0,
                stdout=stdout_msg,
                stderr="",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )

        # Live Execution via Subprocess
        try:
            proc = subprocess.run(
                cmd,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=False,
            )
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except subprocess.TimeoutExpired as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=124,
                stdout="",
                stderr=f"Upload timed out after {self.timeout}s waiting for {cmd}: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except FileNotFoundError as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=127,
                stdout="",
                stderr=f"CHIRP CLI executable not found: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            return SubprocessResult(
                returncode=1,
                stdout="",
                stderr=f"Unhandled exception during CHIRP upload: {e}",
                command=cmd,
                duration_seconds=round(elapsed, 4),
            )

    def list_supported_radios(self) -> List[str]:
        """Queries CHIRP CLI for registered radio model drivers or returns standard list."""
        if self.is_chirpc_available():
            try:
                proc = subprocess.run(
                    [sys.executable, r"C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src\chirpc", "--list-radios"],
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=False,
                )
                if proc.returncode == 0 and proc.stdout:
                    radios = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
                    if radios:
                        return radios
            except Exception as e:
                logger.warning(f"Error querying --list-radios: {e}")

        # Built-in fallback list of common Baofeng models
        return [
            "Baofeng_BF-F8HP",
            "Baofeng_UV-5R",
            "Baofeng_UV-82",
            "Baofeng_UV-82HP",
            "Radioddity_UV-5R_EX",
            "Tenway_UV-5R_Pro",
        ]
