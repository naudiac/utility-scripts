"""
wbr_update.py — WBR Weekly Global Rail Congestion Report Helper Script
-----------------------------------------------------------------------
Run steps individually. The agent will pause between steps to show you
summaries and wait for your confirmation before proceeding.

Subcommands:
  scan_intake     Scan intake folder and report what files are present
  fetch_gocomet   Scrape GoComet and save live port congestion to JSON
  calc_dwell      Calculate Kenvue intermodal dwell stats from GWS file
  show_summary    Display a full before/after table for user confirmation
  update_script   Patch generate_today_congestion.py with confirmed values
  run_generator   Execute generate_today_congestion.py to produce the Excel output
"""

import argparse
import json
import math
import os
import sys
import datetime
import subprocess
import shutil
import re

WORKSPACE = r"c:\Users\whanusiewicz\Documents\Cheryl Lee\Weekly Global Report - Ocean\CESAR File\WBR"
INTAKE_DIR  = os.path.join(WORKSPACE, "intake")
OUTPUT_DIR  = os.path.join(WORKSPACE, "output")
ARCHIVE_DIR = os.path.join(WORKSPACE, "archive")
SCRIPT_PATH = os.path.join(WORKSPACE, "generate_today_congestion.py")
JSON_PATH   = os.path.join(WORKSPACE, "next_data_snippet.json")

LANE_MAP = {
    "FONTANA, CA":   "LAX",
    "LEBANON, PA":   "NY",
    "PALMETTO, GA":  "SAV",
    "BRAMPTON, ON":  "VAN",
    "ETOBICOKE, ON": "MTL",
}

PORT_CODES = {
    "LAX": "USLAX", "LGB": "USLGB", "NY": "USNYC",
    "SAV": "USSAV", "CHS": "USCHS", "PHL": "USPHL",
    "VAN": "CAVAN", "MTL": "CAMTR", "PRR": "CAPRR",
    "HAL": "CAHAL", "SJB": "CASJB",
}

OUTLIER_THRESHOLD = 15  # days — flag anything above this for user review

# ── helpers ──────────────────────────────────────────────────────────────────

def today_str():
    return datetime.date.today().strftime("%Y-%m-%d")

def output_path(args, default_name):
    if hasattr(args, "output") and args.output:
        return args.output
    return os.path.join(WORKSPACE, "tmp_wbr_" + default_name + ".json")

# ── subcommand: scan_intake ───────────────────────────────────────────────────

def cmd_scan_intake(args):
    files = [f for f in os.listdir(INTAKE_DIR) if not os.path.isdir(os.path.join(INTAKE_DIR, f))]
    gws_files   = [f for f in files if f.endswith(".xlsx")]
    image_files = [f for f in files if f.endswith((".webp", ".png", ".jpg"))]
    other_files = [f for f in files if f not in gws_files and f not in image_files]

    result = {
        "scan_date": today_str(),
        "gws_files": gws_files,
        "image_files": image_files,
        "other_files": other_files,
        "intake_dir": INTAKE_DIR,
    }

    if not gws_files:
        result["warning"] = "No GWS Excel file found in intake. Cannot proceed."
    else:
        # Detect most recent GWS file by name
        result["selected_gws_file"] = sorted(gws_files)[-1]

    out = output_path(args, "scan_intake")
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Intake scan complete. Results written to: {out}")
    print(f"  GWS files found    : {gws_files}")
    print(f"  Image files found  : {image_files}")
    if gws_files:
        print(f"  Selected GWS file  : {result['selected_gws_file']}")
    if "warning" in result:
        print(f"  WARNING: {result['warning']}")
    return result

# ── subcommand: fetch_gocomet ─────────────────────────────────────────────────

def cmd_fetch_gocomet(args):
    """Delegate to fetch_live_congestion.py in the scratch folder."""
    scraper = r"C:\Users\whanusiewicz\.gemini\antigravity\scratch\fetch_live_congestion.py"
    if not os.path.exists(scraper):
        print(f"ERROR: GoComet scraper not found at {scraper}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, scraper],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    # Read the refreshed JSON and extract port delays
    if not os.path.exists(JSON_PATH):
        print("ERROR: next_data_snippet.json not found after scrape.", file=sys.stderr)
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    ports_raw = data["props"]["pageProps"]["ssrCongestionData"]
    congestion = {}
    for code, gocomet_code in PORT_CODES.items():
        match = [p for p in ports_raw if p["port"].get("code", "").upper() == gocomet_code.upper()]
        if match:
            congestion[code] = int(round(match[0]["port"].get("delay", 0)))
        else:
            congestion[code] = 0

    out_data = {"fetch_date": today_str(), "congestion": congestion}
    out = output_path(args, "gocomet")
    with open(out, "w") as f:
        json.dump(out_data, f, indent=2)

    print(f"\nLive GoComet port congestion ({today_str()}):")
    for port, days in congestion.items():
        print(f"  {port:<4}: {days} day(s)")
    print(f"\nResults written to: {out}")
    return out_data

# ── subcommand: calc_dwell ────────────────────────────────────────────────────

def cmd_calc_dwell(args):
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas is required. Run: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

    gws_file = args.gws_file
    if not gws_file:
        # Auto-detect
        files = [f for f in os.listdir(INTAKE_DIR) if f.endswith(".xlsx")]
        if not files:
            print("ERROR: No GWS Excel file found in intake.", file=sys.stderr)
            sys.exit(1)
        gws_file = sorted(files)[-1]

    gws_path = os.path.join(INTAKE_DIR, gws_file)
    print(f"Reading GWS file: {gws_path}")

    df = pd.read_excel(gws_path, sheet_name="GWS Report template")
    weeks = sorted(df["Shipment Report Week"].dropna().unique().tolist())
    print(f"Weeks present: {weeks[-6:]}")

    # Identify the two most recent weeks
    current_week  = int(weeks[-1])
    previous_week = int(weeks[-2]) if len(weeks) >= 2 else None

    results = {}
    outlier_flags = []

    for target_week in ([previous_week, current_week] if previous_week else [current_week]):
        df_w = df[df["Shipment Report Week"] == target_week].copy()
        df_w["Discharge Date"] = pd.to_datetime(df_w["Discharge Date"], errors="coerce")
        df_w["Gate Out Date"]  = pd.to_datetime(df_w["Gate Out Date"],  errors="coerce")
        if "Actual delivery to door date" in df_w.columns:
            df_w["Actual delivery to door date"] = pd.to_datetime(df_w["Actual delivery to door date"], errors="coerce")
            df_w["Gate Out Date"] = df_w["Gate Out Date"].fillna(df_w["Actual delivery to door date"])
        df_w["Dwell"] = (df_w["Gate Out Date"] - df_w["Discharge Date"]).dt.days

        week_results = {}
        for city, code in LANE_MAP.items():
            rows = df_w[df_w["Dest City"].str.upper() == city.upper()].copy()
            if "Service type" in rows.columns:
                ptd       = rows[rows["Service type"].str.upper().str.contains("PORT TO DOOR|PTD", na=False)]
                rows_chk  = rows[~rows["Service type"].str.upper().str.contains("PORT TO DOOR|PTD", na=False)]
            else:
                ptd, rows_chk = pd.DataFrame(), rows

            valid    = rows_chk[rows_chk["Dwell"].notnull() & (rows_chk["Dwell"] >= 0)]
            over_15  = valid[valid["Dwell"] > OUTLIER_THRESHOLD]
            clean    = valid[valid["Dwell"] <= OUTLIER_THRESHOLD]

            # Flag outliers for user review (include BOL and comment)
            for _, row in over_15.iterrows():
                bol     = row.get("BOL NO", "UNKNOWN")
                comment = str(row.get("Comments ", "")).strip()
                reason  = str(row.get("Reason for In-Transit delay (Internal data)", "")).strip()
                outlier_flags.append({
                    "week": target_week,
                    "lane": code,
                    "bol": bol,
                    "dwell_days": float(row["Dwell"]),
                    "comment": comment if comment and comment != "nan" else "",
                    "reason": reason if reason and reason != "nan" else "",
                })

            vals = clean["Dwell"].tolist()
            mean = clean["Dwell"].mean() if len(clean) > 0 else None
            rounded = math.ceil(mean) if mean is not None else None

            week_results[code] = {
                "total_rows": len(rows),
                "ptd_excluded": len(ptd),
                "valid_completions": len(valid),
                "outliers_flagged": len(over_15),
                "clean_vals": vals,
                "dwell_days": rounded,
            }

        results[str(target_week)] = week_results

    out_data = {
        "calc_date": today_str(),
        "gws_file": gws_file,
        "current_week": current_week,
        "previous_week": previous_week,
        "dwell_by_week": results,
        "outliers_for_review": outlier_flags,
    }

    out = output_path(args, "dwell")
    with open(out, "w") as f:
        json.dump(out_data, f, indent=2)

    print(f"\n=== DWELL CALCULATION RESULTS ===")
    for wk, lanes in results.items():
        print(f"\nWeek {wk}:")
        for lane, stats in lanes.items():
            dwell = stats["dwell_days"]
            note  = f"{stats['clean_vals']} => {dwell} day(s)" if dwell is not None else "NO COMPLETIONS"
            print(f"  {lane:<4}: {note}  (total={stats['total_rows']}, PTD={stats['ptd_excluded']}, outliers={stats['outliers_flagged']})")

    if outlier_flags:
        print(f"\n{'='*60}")
        print(f"  *** {len(outlier_flags)} OUTLIER(S) FLAGGED FOR USER REVIEW ***")
        print(f"{'='*60}")
        for flag in outlier_flags:
            print(f"  Week {flag['week']} | {flag['lane']} | BOL: {flag['bol']} | Dwell: {flag['dwell_days']} days")
            if flag["comment"]:
                print(f"    Comment: {flag['comment']}")
            if flag["reason"]:
                print(f"    Reason:  {flag['reason']}")
        print(f"\n  ACTION REQUIRED: Review the above outliers.")
        print(f"  Tell me which BOLs to EXCLUDE and I will recalculate accordingly.")
    else:
        print("\nNo outliers detected. All completions are within the 15-day threshold.")

    print(f"\nFull dwell data written to: {out}")
    return out_data

# ── subcommand: show_summary ──────────────────────────────────────────────────

def cmd_show_summary(args):
    """Load gocomet + dwell JSONs and produce a confirmation table."""
    gocomet_file = args.gocomet_file
    dwell_file   = args.dwell_file
    excluded     = args.exclude or []

    with open(gocomet_file) as f:
        gocomet_data = json.load(f)
    with open(dwell_file) as f:
        dwell_data = json.load(f)

    congestion   = gocomet_data["congestion"]
    current_week = dwell_data["current_week"]
    prev_week    = str(dwell_data.get("previous_week", ""))
    dwell_by_wk  = dwell_data["dwell_by_week"]

    # Determine dwell per lane: use current week if available, else previous
    lane_dwells = {}
    for lane in ["LAX", "LGB", "NY", "SAV", "CHS", "PHL", "VAN", "MTL", "PRR", "HAL", "SJB"]:
        curr = dwell_by_wk.get(str(current_week), {}).get(lane, {})
        prev = dwell_by_wk.get(prev_week, {}).get(lane, {})
        if curr.get("dwell_days") is not None:
            dwell = curr["dwell_days"]
            source = f"W{current_week} actuals"
        elif prev.get("dwell_days") is not None:
            dwell = prev["dwell_days"]
            source = f"W{prev_week} carry-forward"
        else:
            dwell = "TBD"
            source = "no completions"
        lane_dwells[lane] = {"dwell": dwell, "source": source}

    # PHL always TBD until established
    lane_dwells["PHL"] = {"dwell": "TBD (MKT EST 5)", "source": "new lane"}

    print(f"\n{'='*75}")
    print(f"  WBR CONGESTION REPORT SUMMARY — {today_str()}")
    print(f"  PLEASE REVIEW AND CONFIRM BEFORE THE SCRIPT IS UPDATED")
    print(f"{'='*75}")
    print(f"{'Port':<6} {'GoComet Congestion':>20} {'Kenvue Dwell':>15} {'Source':>25}")
    print(f"{'-'*6} {'-'*20} {'-'*15} {'-'*25}")
    for lane in ["LAX", "LGB", "NY", "SAV", "CHS", "PHL", "VAN", "MTL", "PRR", "HAL", "SJB"]:
        cong  = congestion.get(lane, "N/A")
        info  = lane_dwells[lane]
        excl  = " [EXCLUDED]" if lane in excluded else ""
        print(f"{lane:<6} {str(cong) + ' days':>20} {str(info['dwell']):>15} {info['source']:>25}{excl}")

    print(f"\nExcluded BOLs: {excluded if excluded else 'None'}")
    print(f"\nACTION: Review the table above. If everything looks correct, tell me")
    print(f"  to proceed with 'update the script'. If you want to exclude a BOL or")
    print(f"  adjust a dwell value, tell me and I will recalculate.\n")

    out_data = {
        "summary_date": today_str(),
        "current_week": current_week,
        "congestion": congestion,
        "lane_dwells": lane_dwells,
        "excluded_bols": excluded,
    }
    out = output_path(args, "summary")
    with open(out, "w") as f:
        json.dump(out_data, f, indent=2)
    print(f"Summary written to: {out}")
    return out_data

# ── subcommand: run_generator ─────────────────────────────────────────────────

def cmd_run_generator(args):
    print(f"Running: {SCRIPT_PATH}")
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH],
        cwd=WORKSPACE,
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    today = datetime.date.today().strftime("%m-%d-%Y")
    # Monday date logic: if today is not Wednesday, use the most recent Wednesday
    expected_output = os.path.join(OUTPUT_DIR, f"Congestion-{today_str().replace('-', '-')[5:]}-{today_str()[:4]}.xlsx")
    print(f"\nGenerator complete. Check output/ folder for today's Congestion report.")
    # Play notification sound
    subprocess.run(
        ["powershell", "-c", "(New-Object Media.SoundPlayer 'C:\\Windows\\Media\\Windows Notify System Generic.wav').PlaySync()"],
        check=False
    )

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="wbr_update",
        description="WBR Weekly Global Rail Congestion Report — step-by-step update helper"
    )
    sub = parser.add_subparsers(dest="command")

    # scan_intake
    p1 = sub.add_parser("scan_intake", help="Scan the intake folder and identify files")
    p1.add_argument("--output", help="Output JSON path")

    # fetch_gocomet
    p2 = sub.add_parser("fetch_gocomet", help="Scrape GoComet for live port congestion data")
    p2.add_argument("--output", help="Output JSON path")

    # calc_dwell
    p3 = sub.add_parser("calc_dwell", help="Calculate Kenvue intermodal dwell from GWS file")
    p3.add_argument("--gws-file", default=None, help="GWS Excel filename in intake/ (auto-detected if omitted)")
    p3.add_argument("--output", help="Output JSON path")

    # show_summary
    p4 = sub.add_parser("show_summary", help="Display confirmation table before updating the script")
    p4.add_argument("--gocomet-file", required=True, help="Path to fetch_gocomet output JSON")
    p4.add_argument("--dwell-file",   required=True, help="Path to calc_dwell output JSON")
    p4.add_argument("--exclude", nargs="*", default=[], help="BOL numbers to exclude from dwell calc")
    p4.add_argument("--output", help="Output JSON path")

    # run_generator
    p5 = sub.add_parser("run_generator", help="Run generate_today_congestion.py to produce today's Excel output")

    args = parser.parse_args()

    if args.command == "scan_intake":
        cmd_scan_intake(args)
    elif args.command == "fetch_gocomet":
        cmd_fetch_gocomet(args)
    elif args.command == "calc_dwell":
        cmd_calc_dwell(args)
    elif args.command == "show_summary":
        cmd_show_summary(args)
    elif args.command == "run_generator":
        cmd_run_generator(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
