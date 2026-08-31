"""Example usage script for baofeng-headless-programmer.

Demonstrates programmatic usage of:
1. Dynamic frequency fetching and plan synthesis for zip code 30445.
2. CHIRP CSV serialization and validation.
3. Subprocess driver mock execution and backup creation.
4. Production pipeline invocation.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path
SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from chirp_driver import ChirpDriver
from csv_engine import CSVEngine
from frequency_fetcher import FrequencyFetcher
from baofeng_programmer import run_pipeline


def main() -> None:
    print("=== Baofeng Headless Programmer Example Usage ===")

    # 1. Initialize Frequency Fetcher and query zip 30445
    print("\n[Step 1] Sourcing local frequencies for Metter, GA (Zip 30445)...")
    fetcher = FrequencyFetcher()
    plan = fetcher.build_frequency_plan(
        zip_code="30445",
        max_total_channels=128,
        mock=True,
        radius_miles=35.0,
        bands=["2m", "70cm"],
    )
    print(f"Generated {len(plan)} total channels.")
    for ch in plan[:5]:
        print(f"  Slot {ch.location:03d}: {ch.name:<7s} | {ch.frequency:.4f} MHz | Duplex: {ch.duplex or 'Simplex'} | Mode: {ch.mode}")

    # 2. Export plan to CHIRP-compatible CSV
    print("\n[Step 2] Exporting plan to CHIRP-compatible CSV...")
    csv_engine = CSVEngine()
    out_csv = SKILL_ROOT / "examples" / "sample_30445_plan.csv"
    csv_engine.export_csv(plan, out_csv)
    is_valid, errors = csv_engine.validate_csv_file(out_csv)
    print(f"Exported to {out_csv} (Valid: {is_valid})")

    # 3. Simulate full programming pipeline via run_pipeline
    print("\n[Step 3] Executing simulated programming pipeline...")
    backup_dir = SKILL_ROOT / "examples" / "backups"
    result = run_pipeline(
        zip_code="30445",
        port="COM3",
        dry_run=True,
        mock=True,
        output_csv=out_csv,
        backup_dir=backup_dir,
        radio_model="Baofeng_BF-F8HP",
    )
    print(f"Pipeline Result Status: {result.get('status')}")
    print(f"Channels Programmed: {result.get('channels_count')}")
    print(f"Backup Image: {result.get('backup_file')}")
    print(f"Message: {result.get('message')}")
    print("\n=== Example Completed Successfully ===")


if __name__ == "__main__":
    main()
