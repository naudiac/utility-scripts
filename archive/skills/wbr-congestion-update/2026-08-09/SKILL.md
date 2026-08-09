---
name: wbr-congestion-update
description: >-
  Weekly update skill for the WINA Global Rail Congestion Report (WBR).
  Triggered by "update wbr". Scans the intake folder for the current week's
  GWS Excel file, fetches live GoComet port congestion data, calculates
  Kenvue intermodal dwell per lane, flags outliers for user confirmation,
  then updates generate_today_congestion.py and produces the weekly
  Congestion-MM-DD-YYYY.xlsx output file. Pauses at each decision checkpoint
  (dwell values, outlier exclusions, commentary) before applying changes.
---

# WBR Weekly Congestion Report Update

## Overview

This skill handles the full **Wednesday WBR report pipeline** for the WINA
Global Rail Congestion Report. It runs step-by-step with explicit user
confirmation at each key decision point — dwell values, outlier exclusions,
and commentary — before writing anything to the output file.

**Trigger phrases:** "update wbr", "provide today's update", "run the wbr",
"generate the congestion report", "it's Wednesday, ready?"

## Workspace

All paths are relative to the WBR workspace root:
```
c:\Users\whanusiewicz\Documents\Cheryl Lee\Weekly Global Report - Ocean\CESAR File\WBR\
  intake/           ← drop new GWS .xlsx files here each week
  output/           ← generated Congestion-MM-DD-YYYY.xlsx lands here
  archive/          ← previous outputs and processed GWS files are moved here
  generate_today_congestion.py  ← the report generator (updated each week)
  next_data_snippet.json        ← live GoComet congestion cache
```

## Helper Script

**Location:** `.agents/skills/wbr-congestion-update/scripts/wbr_update.py`

Run with: `python wbr_update.py <subcommand> [options]`

### Subcommands

| Subcommand | Purpose |
|---|---|
| `scan_intake` | Scan intake/ and identify GWS file + any image files |
| `fetch_gocomet` | Scrape GoComet for live port congestion data |
| `calc_dwell` | Parse GWS file and calculate Kenvue intermodal dwell per lane |
| `show_summary` | Display confirmation table (congestion + dwell) before updating |
| `run_generator` | Execute generate_today_congestion.py to produce the Excel output |

## Workflow

When "update wbr" (or equivalent) is triggered, execute these steps **in order**, pausing at each checkpoint marked ⏸.

---

### Step 1 — Scan Intake

```
python .agents/skills/wbr-congestion-update/scripts/wbr_update.py scan_intake --output tmp_scan.json
```

Report what GWS file was found. If no GWS file is present, **STOP** and tell
the user: "No GWS file found in intake. Please drop the current week's GWS
Excel file into the intake/ folder and try again."

If image files (`.webp`, `.png`) are present, note them but do NOT process
them — tell the user "WALKER images found — ask me to embed them separately."

---

### Step 2 — Fetch Live GoComet Data

```
python .agents/skills/wbr-congestion-update/scripts/wbr_update.py fetch_gocomet --output tmp_gocomet.json
```

This calls the GoComet scraper at:
`C:\Users\whanusiewicz\.gemini\antigravity\scratch\fetch_live_congestion.py`

If the scraper fails, check network/VPN status. Do NOT fabricate congestion values.

---

### Step 3 — Calculate Kenvue Dwell ⏸

```
python .agents/skills/wbr-congestion-update/scripts/wbr_update.py calc_dwell --output tmp_dwell.json
```

**Exclusion rules (applied automatically):**
- PTD (Port-to-Door) service type shipments are always excluded from dwell
- Shipments with `Dwell = NaN` (Gate Out Date not yet set) are excluded
- Any dwell value > 15 days is **flagged as an outlier**

**⏸ CHECKPOINT — Outlier Review:**
After running `calc_dwell`, check the output for `outliers_for_review`. If any
exist, display them to the user in this format:

```
⚠️  OUTLIER FLAGGED FOR REVIEW
  Week [W] | Lane: [LANE] | BOL: [BOL_NUMBER] | Dwell: [X] days
  Comment: [GWS comment field]
  Reason: [GWS reason code field]

→ Should this shipment be EXCLUDED from the dwell average? (yes/no)
```

Wait for the user's answer for **each** outlier before proceeding.
If excluded, note the BOL number for the `--exclude` flag in Step 4.

---

### Step 4 — Show Summary Table ⏸

```
python .agents/skills/wbr-congestion-update/scripts/wbr_update.py show_summary \
  --gocomet-file tmp_gocomet.json \
  --dwell-file tmp_dwell.json \
  [--exclude BOL1 BOL2 ...] \
  --output tmp_summary.json
```

This displays a full before/after table with all 11 ports showing:
- Live GoComet congestion (days)
- Kenvue dwell (days, with source: actuals vs. carry-forward)

**⏸ CHECKPOINT — Full Confirmation:**
Present the table and ask: "Does everything look correct? If so, I'll update
the generator script and produce today's output. If you'd like to adjust any
dwell value manually, let me know."

Wait for explicit "proceed" / "looks good" / "yes" before continuing.

---

### Step 5 — Update generate_today_congestion.py ⏸

Using the confirmed values from `tmp_summary.json`, update these sections in
`generate_today_congestion.py`:

1. **File names** — `old_file` (last week's output) and `new_file` (today's date)
2. **Date cell** — `sheet1["A1"] = "YYYY-MM-DD"` (today)
3. **Fallback congestion dict** — update all 11 port values
4. **`updated_data` dict** — update all 11 ports with confirmed congestion + dwell values
5. **Commentary** (rows 15–18) — update all 4 regional paragraphs
6. **Value-add bullets** (row 20) — update the executive summary bullets
7. **Archive section** — update filenames for old output + GWS file

**Dwell carry-forward rule:**
- If a lane has confirmed actuals from the current or previous week → use them
- If no completions at all → carry the value from the last report unchanged
- PHL always stays as `TBD (MKT EST 5)` / `TBD (MKT EST 3)` until GWS history exists

**Commentary writing rules:**
- Do NOT reference internal process names (e.g., "baseline carry-forward", "GWS export")
- Use clean executive language: "confirmed by this week's actuals", "no change from prior week"
- Highlight the biggest mover (largest congestion change week-over-week) in the alert bullets
- Note any Montreal / Vancouver spikes specifically — these are leadership focus ports

**⏸ CHECKPOINT — Commentary Draft Review:**
Before writing the commentary to the file, display your draft commentary for all
4 regions and the value-add bullets. Ask the user: "Does this commentary look
right? Say 'proceed' to write it to the script."

---

### Step 6 — Run the Generator

```
python .agents/skills/wbr-congestion-update/scripts/wbr_update.py run_generator
```

This executes `generate_today_congestion.py` which:
- Copies the prior week's Excel as the new template
- Fills in all port values (congestion, dwell, rail delays)
- Writes regional commentary and value-add bullets
- Rebuilds the Executive_Dashboard tab
- Saves `Congestion-MM-DD-YYYY.xlsx` to `output/`
- Archives the previous output and GWS intake files

On success, play the Windows notification chime and report:
`✅ Congestion-[date].xlsx is ready in output/`

---

### Step 7 — Cleanup

Delete the temporary JSON files (`tmp_scan.json`, `tmp_gocomet.json`,
`tmp_dwell.json`, `tmp_summary.json`) from the workspace root.

---

## Port Reference

| Code | Port | GoComet Code |
|---|---|---|
| LAX | Los Angeles | USLAX |
| LGB | Long Beach | USLGB |
| NY | New York/NJ | USNYC |
| SAV | Savannah | USSAV |
| CHS | Charleston | USCHS |
| PHL | Philadelphia | USPHL |
| VAN | Vancouver | CAVAN |
| MTL | Montreal | CAMTR |
| PRR | Prince Rupert | CAPRR |
| HAL | Halifax | CAHAL |
| SJB | Saint John | CASJB |

## Lane → Dest City Mapping (GWS file)

| Code | GWS Dest City | Notes |
|---|---|---|
| LAX | FONTANA, CA | Exclude PTD rows |
| NY | LEBANON, PA | Exclude PTD rows |
| SAV | PALMETTO, GA | All rows included |
| VAN | BRAMPTON, ON | Exclude PTD rows |
| MTL | ETOBICOKE, ON | Exclude PTD rows |
| PHL | — | No GWS history yet — always TBD |
| LGB, CHS, PRR, HAL, SJB | — | No GWS lane data — baseline only |

## Dwell Calculation Rules

1. **Filter by Dest City** using the lane map above
2. **Exclude PTD** (Service type contains "PORT TO DOOR" or "PTD")
3. **Exclude rows** where `Gate Out Date` is blank (shipment not yet retrieved)
4. **Calculate:** `Dwell = Gate Out Date − Discharge Date` (in days)
5. **Flag outliers:** Any dwell > 15 days → present to user for include/exclude decision
6. **Average and round up** (`math.ceil`) the clean values
7. **Carry forward** if no clean completions exist for the current week

## Common Mistakes

1. **Don't use internal process language in commentary** — never say "carry-forward",
   "baseline", or "GWS export". Use clean executive language.
2. **Don't skip the outlier review** — always check `outliers_for_review` in the
   `calc_dwell` JSON output. A 12-day dwell from a customs hold is very different
   from a true 12-day intermodal delay.
3. **Don't forget to update the archive filenames** in `generate_today_congestion.py`
   — both the prev output filename AND the GWS intake filename must be updated
   each week or the archive step will silently fail.
