"""Production CLI Entrypoint for Baofeng BF-F8HP Headless Programmer.

Automates reading, dynamic frequency sourcing (NOAA, RepeaterBook, GMRS, Simplex),
merging, and writing radio memory configurations headlessly via CHIRP CLI.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from .models import ChannelEntry, FrequencyPlan, GeoLocation, RepeaterInfo, SubprocessResult
    from .chirp_driver import ChirpDriver, ChirpDriverError, RadioCommunicationError, RadioTimeoutError
    from .frequency_fetcher import FrequencyFetcher
    from .csv_engine import CSVEngine
except (ImportError, ValueError):
    from models import ChannelEntry, FrequencyPlan, GeoLocation, RepeaterInfo, SubprocessResult
    from chirp_driver import ChirpDriver, ChirpDriverError, RadioCommunicationError, RadioTimeoutError
    from frequency_fetcher import FrequencyFetcher
    from csv_engine import CSVEngine

# Exit Codes
EXIT_SUCCESS: int = 0
EXIT_GENERAL_ERROR: int = 1
EXIT_COM_PORT_ERROR: int = 2
EXIT_API_ERROR: int = 3
EXIT_CAPACITY_OVERFLOW: int = 4

logger = logging.getLogger("baofeng_programmer")


def build_parser() -> argparse.ArgumentParser:
    """Constructs the production CLI argument parser with subcommands and flag combinations."""
    parser = argparse.ArgumentParser(
        prog="baofeng_programmer",
        description="Headless Programmer & Automated Frequency Sourcing for Baofeng BF-F8HP / UV-5R radios.",
    )

    def add_common_arguments(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--zip",
            dest="zip",
            type=str,
            default=None,
            help="5-digit US Postal Zip Code for location-based repeater & NOAA lookup.",
        )
        p.add_argument(
            "--port",
            dest="port",
            type=str,
            default=None,
            help="Serial COM port connected to the radio programming cable (e.g. COM3, /dev/ttyUSB0).",
        )
        p.add_argument(
            "--radio-model",
            dest="radio_model",
            type=str,
            default="Baofeng_BF-F8HP",
            help="Radio model identifier for CHIRP driver (default: Baofeng_BF-F8HP).",
        )
        p.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_true",
            default=False,
            help="Simulate execution and subprocess commands without communicating with physical hardware.",
        )
        p.add_argument(
            "--mock",
            dest="mock",
            action="store_true",
            default=False,
            help="Use offline mock datasets and synthetic memory images for CI and testing.",
        )
        p.add_argument(
            "--output-csv",
            dest="output_csv",
            type=str,
            default=None,
            help="Path to save the generated CHIRP-compatible CSV channel plan.",
        )
        p.add_argument(
            "--backup-dir",
            dest="backup_dir",
            type=str,
            default=None,
            help="Directory path where timestamped radio memory backups (.img) are saved.",
        )
        p.add_argument(
            "--radius",
            dest="radius",
            type=float,
            default=35.0,
            help="Search radius in miles for nearby repeater discovery (default: 35.0).",
        )
        p.add_argument(
            "--start-channel",
            dest="start_channel",
            type=int,
            default=1,
            help="Starting memory slot index for local amateur repeaters (default: 1).",
        )
        p.add_argument(
            "--max-channels",
            dest="max_channels",
            type=int,
            default=128,
            help="Maximum total memory channel capacity (hard limit: 128 for BF-F8HP).",
        )
        p.add_argument(
            "--bands",
            dest="bands",
            type=str,
            default="2m,70cm",
            help="Comma-separated amateur radio frequency bands to include (e.g. '2m,70cm').",
        )
        p.add_argument(
            "--power",
            dest="power",
            type=str,
            default="High",
            choices=["High", "Med", "Low"],
            help="Default transmit power level for repeaters and simplex channels.",
        )
        p.add_argument(
            "--json",
            dest="json",
            action="store_true",
            default=False,
            help="Output execution status and details formatted as structured JSON.",
        )
        p.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Enable verbose debug output and detailed logging.",
        )
        p.add_argument(
            "--token",
            dest="token",
            type=str,
            default=None,
            help="Optional RepeaterBook API authentication token.",
        )
        p.add_argument(
            "--fetch-only",
            dest="fetch_only",
            action="store_true",
            default=False,
            help="Only query APIs and generate frequency plan / CSV without radio communication.",
        )
        p.add_argument(
            "--download-only",
            dest="download_only",
            action="store_true",
            default=False,
            help="Only download and backup radio memory image without modifying.",
        )
        p.add_argument(
            "--upload-only",
            dest="upload_only",
            action="store_true",
            default=False,
            help="Only upload an existing image or CSV to the radio.",
        )
        p.add_argument(
            "--input-file",
            dest="input_file",
            type=str,
            default=None,
            help="Path to input CSV or .img file for upload-only operations.",
        )

    add_common_arguments(parser)

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    p_fetch = subparsers.add_parser("fetch", help="Fetch local frequencies and export CSV")
    add_common_arguments(p_fetch)

    p_download = subparsers.add_parser("download", help="Download radio memory image to file")
    add_common_arguments(p_download)

    p_upload = subparsers.add_parser("upload", help="Upload memory image or CSV to radio")
    add_common_arguments(p_upload)

    p_program = subparsers.add_parser("program", help="Full automated read-merge-write workflow")
    add_common_arguments(p_program)

    return parser


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parses command-line arguments and returns namespace."""
    parser = build_parser()
    return parser.parse_args(args)


def run_pipeline(
    zip_code: Optional[str] = None,
    port: Optional[str] = None,
    dry_run: bool = False,
    mock: bool = False,
    output_csv: Optional[Union[str, Path]] = None,
    backup_dir: Optional[Union[str, Path]] = None,
    radio_model: str = "Baofeng_BF-F8HP",
    radius: float = 35.0,
    start_channel: int = 1,
    max_channels: int = 128,
    bands: Optional[Union[str, List[str]]] = None,
    power: str = "High",
    token: Optional[str] = None,
    fetch_only: bool = False,
    download_only: bool = False,
    upload_only: bool = False,
    input_file: Optional[Union[str, Path]] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Executes the full Baofeng programming pipeline.

    Steps:
        1. Validate inputs and radio capacity limits.
        2. If port is provided (and not fetch_only): download image and create verified timestamped backup.
        3. If zip_code is provided: query NOAA, VHF Calling, GMRS 1-22, and active On-Air repeaters.
        4. Synthesize frequency plan and export valid 19-column CHIRP CSV.
        5. If port is provided (and not fetch_only / download_only): upload configuration to radio.
        6. Return execution status dictionary.

    Returns:
        Dictionary containing status ('success' or 'error'), returncode, output paths, and metadata.
    """
    start_time = time.perf_counter()

    radius_val = float(radius) if radius is not None else 35.0
    max_chans = int(max_channels) if max_channels is not None else 128
    start_ch = int(start_channel) if start_channel is not None else 1

    band_list: Optional[List[str]] = None
    if bands:
        if isinstance(bands, str):
            band_list = [b.strip() for b in bands.split(",") if b.strip()]
        elif isinstance(bands, list):
            band_list = bands

    # Capacity check (Hard hardware limit: 128 channels)
    if max_chans > 128 or max_chans <= 0:
        return {
            "status": "error",
            "returncode": EXIT_CAPACITY_OVERFLOW,
            "error_type": "CapacityOverflowError",
            "message": f"Invalid channel capacity {max_chans}. Baofeng BF-F8HP has a hard limit of 128 memory channels (0..127).",
            "channels_count": 0,
        }

    chirp_driver = ChirpDriver()
    frequency_fetcher = FrequencyFetcher(repeaterbook_token=token)
    csv_engine = CSVEngine()

    backup_path: Optional[Path] = None
    csv_dest: Optional[Path] = Path(output_csv) if output_csv else None
    plan: Optional[List[ChannelEntry]] = None
    download_result: Optional[SubprocessResult] = None
    upload_result: Optional[SubprocessResult] = None
    raw_download_img: Optional[Path] = None

    # Step 1: Headless Download & Timestamped Backup (if port specified)
    if port and not fetch_only and not upload_only:
        b_dir = Path(backup_dir) if backup_dir else Path("./backups")
        b_dir.mkdir(parents=True, exist_ok=True)
        raw_download_img = b_dir / f"download_{radio_model}_temp.img"

        try:
            download_result = chirp_driver.download_radio_image(
                port=port,
                output_path=raw_download_img,
                model=radio_model,
                dry_run=dry_run,
                mock=mock,
            )
            if download_result.returncode != 0:
                return {
                    "status": "error",
                    "returncode": EXIT_COM_PORT_ERROR,
                    "error_type": "RadioCommunicationError",
                    "message": f"Failed to download memory image from radio on port {port}: {download_result.stderr}",
                    "download_result": download_result,
                }

            # Create timestamped verified backup
            backup_path = chirp_driver.create_backup(
                source_path=raw_download_img,
                backup_dir=b_dir,
                prefix=f"backup_{radio_model}",
            )
        except Exception as e:
            return {
                "status": "error",
                "returncode": EXIT_COM_PORT_ERROR,
                "error_type": "RadioCommunicationError",
                "message": f"Error during radio download / backup on port {port}: {e}",
            }

        if download_only:
            return {
                "status": "success",
                "returncode": EXIT_SUCCESS,
                "message": f"Successfully downloaded and backed up radio image to {backup_path}",
                "backup_file": str(backup_path),
                "port": port,
                "radio_model": radio_model,
                "download_result": download_result,
            }

    # Step 2: Dynamic Frequency Sourcing & Plan Synthesis (if zip_code provided)
    if zip_code and not download_only and not upload_only:
        clean_zip = str(zip_code).strip()
        if not frequency_fetcher.is_valid_zip_code(clean_zip) and not mock:
            return {
                "status": "error",
                "returncode": EXIT_API_ERROR,
                "error_type": "InvalidZipCodeError",
                "message": f"Invalid 5-digit US postal zip code: {zip_code}",
                "channels_count": 0,
            }

        try:
            plan = frequency_fetcher.build_frequency_plan(
                zip_code=clean_zip,
                max_total_channels=max_chans,
                mock=mock,
                repeater_start_channel=start_ch,
                power=power,
                bands=band_list,
                radius_miles=radius_val,
            )
        except Exception as e:
            return {
                "status": "error",
                "returncode": EXIT_API_ERROR,
                "error_type": "FrequencySourcingError",
                "message": f"Failed to source frequencies for zip {zip_code}: {e}",
                "channels_count": 0,
            }

        if len(plan) > 128:
            plan = plan[:128]

        # Export CSV if requested or if output_csv is set
        if csv_dest:
            csv_dest.parent.mkdir(parents=True, exist_ok=True)
            csv_engine.export_csv(plan, csv_dest)
            is_valid, errors = csv_engine.validate_csv_file(csv_dest)
            if not is_valid:
                return {
                    "status": "error",
                    "returncode": EXIT_GENERAL_ERROR,
                    "error_type": "CSVValidationError",
                    "message": f"Generated CSV failed validation: {errors}",
                    "channels_count": len(plan),
                }
        elif not port:
            # Standalone fetch without port
            csv_dest = Path(f"baofeng_plan_{clean_zip}.csv")
            csv_engine.export_csv(plan, csv_dest)

    # Step 3: Safe Writeback & Upload (if port specified and not fetch_only / download_only)
    if port and not fetch_only and not download_only:
        upload_img = raw_download_img if raw_download_img is not None and raw_download_img.exists() else None
        if not upload_img:
            temp_dir = Path(tempfile.gettempdir())
            upload_img = temp_dir / f"upload_{radio_model}_temp.img"
            chirp_driver.generate_mock_image(upload_img, model=radio_model)

        try:
            upload_result = chirp_driver.upload_radio_image(
                port=port,
                input_path=upload_img,
                model=radio_model,
                dry_run=dry_run,
                mock=mock,
            )
            if upload_result.returncode != 0:
                return {
                    "status": "error",
                    "returncode": EXIT_COM_PORT_ERROR,
                    "error_type": "RadioCommunicationError",
                    "message": f"Failed to upload memory image to radio on port {port}: {upload_result.stderr}",
                    "upload_result": upload_result,
                }
        except Exception as e:
            return {
                "status": "error",
                "returncode": EXIT_COM_PORT_ERROR,
                "error_type": "RadioCommunicationError",
                "message": f"Error during radio upload on port {port}: {e}",
            }

    elapsed = time.perf_counter() - start_time
    channels_count = len(plan) if plan is not None else 0

    return {
        "status": "success",
        "returncode": EXIT_SUCCESS,
        "zip_code": zip_code,
        "radio_model": radio_model,
        "port": port,
        "dry_run": dry_run,
        "mock": mock,
        "channels_count": channels_count,
        "output_csv": str(csv_dest) if csv_dest else None,
        "backup_file": str(backup_path) if backup_path else None,
        "duration_seconds": round(elapsed, 4),
        "message": f"Successfully synthesized frequency plan ({channels_count} channels)"
        + (f" and wrote to radio on {port}" if port else f" and saved CSV to {csv_dest}"),
    }


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entrypoint for Baofeng Headless Programmer."""
    args = parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    fetch_only = args.fetch_only or (args.command == "fetch")
    download_only = args.download_only or (args.command == "download")
    upload_only = args.upload_only or (args.command == "upload")

    result = run_pipeline(
        zip_code=args.zip,
        port=args.port,
        dry_run=args.dry_run,
        mock=args.mock,
        output_csv=args.output_csv,
        backup_dir=args.backup_dir,
        radio_model=args.radio_model,
        radius=args.radius,
        start_channel=args.start_channel,
        max_channels=args.max_channels,
        bands=args.bands,
        power=args.power,
        token=args.token,
        fetch_only=fetch_only,
        download_only=download_only,
        upload_only=upload_only,
        input_file=args.input_file,
        verbose=args.verbose,
    )

    if args.json:
        clean_result = dict(result)
        if "download_result" in clean_result and isinstance(clean_result["download_result"], SubprocessResult):
            clean_result["download_result"] = clean_result["download_result"].__dict__
        if "upload_result" in clean_result and isinstance(clean_result["upload_result"], SubprocessResult):
            clean_result["upload_result"] = clean_result["upload_result"].__dict__
        print(json.dumps(clean_result, indent=2))
    else:
        if result.get("status") == "success":
            print(f"[SUCCESS] {result.get('message')}")
            if result.get("output_csv"):
                print(f"  -> CSV File: {result.get('output_csv')}")
            if result.get("backup_file"):
                print(f"  -> Backup Image: {result.get('backup_file')}")
            print(f"  -> Total Channels: {result.get('channels_count')}")
        else:
            print(f"[ERROR] ({result.get('error_type')}) {result.get('message')}", file=sys.stderr)

    return int(result.get("returncode", EXIT_SUCCESS))


if __name__ == "__main__":
    sys.exit(main())
