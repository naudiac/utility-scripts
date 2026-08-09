---
name: wina-kenvue-cli-rebuild
description: >-
  Rebuilds the Container Level Info. tab in the weekly Kenvue GWS report
  (WINA-GWS Report-Week ##-Kenvue.xlsx) from scratch using the GWS Report
  template as the sole source of truth. Populates Kenvue Feedback from
  FEEDBACK.xlsx and auto-classifies Provider's Response. Always writes output
  to a new sheet for comparison. Use when asked to update, align, or refresh
  the Container Level Info. tab against the GWS Report template.
---

# WINA Kenvue — Container Level Info. Rebuild

## Overview

The `Container Level Info.` (CLI) tab must mirror the `GWS Report template` tab
exactly — one row per container, rebuilt fresh from GWS each week.

**Critical rule:** GWS Report template is the **only** source of truth for CLI
structure and data. FEEDBACK.xlsx is used **only** for the Kenvue Feedback column.
Do NOT add extra columns from FEEDBACK.xlsx to CLI (e.g. Shipment Status,
Service type, regions, ETD/ATA dates). CLI always has exactly 18 columns (A–R).

## Why Rebuild Instead of Update

BOL numbers are added, removed, and sometimes changed between weeks.
A diff-based update will produce wrong row counts. Always do a full rebuild.

## Files

| File | Role |
|---|---|
| `WINA-GWS Report-Week ##-Kenvue.xlsx` | Target — contains `GWS Report template` and `Container Level Info.` |
| `FEEDBACK.xlsx` | Source of Kenvue Feedback only |

Both live in:
`C:\Users\whanusiewicz\Documents\Cheryl Lee\Weekly Global Report - Ocean\CESAR File\2023\KENVUE\`

## CLI Column Structure (Always 18 columns, A–R)

| Col | Header | GWS Source Column |
|---|---|---|
| A | Shipment Report Week | Shipment Report Week (F) |
| B | Provider | Provider (G) |
| C | BOL Number | BOL NO (AC) |
| D | Equipment Type | Equipment Type (M) |
| E | Container Type | Container Type (AJ) |
| F | Container Number | Container No. (AD) — note trailing space in col name |
| G | No. of Units (Pallets/Packages) | No. of Units (Pallets/Packages) (AE) |
| H | UOM | UOM (AF) |
| I | Total CBM | Total CMB (AG) — note "CMB" not "CBM" in GWS |
| J | Total Weight in KG | Total Weight in KG (AH) |
| K | Empty Pick up Date | Empty pick-up Date (AU) |
| L | Gate in Date | Gate In Date (AZ) — note trailing space in col name |
| M | Discharge Date | Discharge Date (BK) |
| N | Gate Out Date | Gate Out Date (BM) |
| O | Empty Return Date | Empty return Date (BR) |
| P | Invoice/PO/DN Number | Invoice Number (AI) |
| Q | Kenvue Feedback | FEEDBACK.xlsx CLI — matched by BOL + Container# |
| R | Provider's Response to Kenvue Feedback | Auto-classified (see rules below) |

> [!IMPORTANT]
> The GWS column "Container No. " has a trailing space. The GWS column "Gate In Date "
> also has a trailing space. Always strip column names when matching.
> The GWS column "Total CMB" spells CBM as CMB — this is not a typo, it is the GWS column name.

## Provider's Response Auto-Classification Rules

Apply to each row's Kenvue Feedback text. Split on `/` for multi-part feedback.

| Condition | Response |
|---|---|
| Feedback is blank | *(leave blank)* |
| Feedback = `CU_Missing Total CBM` (alone, nothing else) | `UNAVAILABLE` |
| Any part contains `missing`, `less than`, or `needs to be corrected` | `UNDER REVIEW` |
| Any part starts with `CU_` (and no date keywords) | `EXCEPTION` |
| Anything else unrecognized | `UNDER REVIEW` |

Mixed (CU_ + date issue in same feedback) → `UNDER REVIEW` (date issue takes precedence).

## Workflow

### 1. Back Up the File
```python
shutil.copy2(TARGET, TARGET.replace('.xlsx', '_BACKUP.xlsx'))
```

### 2. Load FEEDBACK.xlsx CLI → Build Feedback Lookup
```python
# Key: (BOL Number, Container Number) → Kenvue Feedback text
fb_map = {(bol, container): feedback_text, ...}
```
Fallback: if exact (BOL, Container#) not found, try BOL-only match.

### 3. Load GWS Report template with pandas
```python
gws_df = pd.read_excel(TARGET, sheet_name='GWS Report template', keep_default_na=False)
```

### 4. Build Output Rows (one per GWS row)
For each GWS row, map columns per the table above, look up feedback by (BOL, Container#),
then classify the response.

### 5. Write to New Sheet
- Sheet name: `'Container Level Info. NEW'`
- Positioned immediately after `'Container Level Info.'` tab
- Copy header style from original CLI row 1
- Copy column widths from original CLI
- Set `freeze_panes = 'A2'`
- Format all date columns as `'DD-MMM-YY'`
- Leave original `Container Level Info.` untouched for comparison

### 6. Verify Before Finalizing
Report counts to user:
- Total rows (should match GWS row count)
- Rows with Kenvue Feedback
- Response breakdown: EXCEPTION / UNDER REVIEW / UNAVAILABLE / blank

**Wait for user to visually confirm the new sheet before renaming or deleting the old one.**

## Common Mistakes (Do Not Repeat)

> [!CAUTION]
> **Do NOT add extra columns from FEEDBACK.xlsx to CLI.** FEEDBACK.xlsx has 34+ columns
> (Shipment Status, Service type, Origin/Dest regions, ETD/ATA dates, concat, max caps, etc.).
> These columns do NOT belong in CLI. CLI always has exactly 18 columns.

> [!CAUTION]
> **Do NOT do a diff-based update.** BOLs are added/removed/renamed between weeks.
> Always rebuild from scratch using GWS as source of truth.

> [!IMPORTANT]
> Always write to `'Container Level Info. NEW'` first. Never overwrite the original
> `'Container Level Info.'` sheet directly until the user has reviewed and approved.

## Reusable Script

The script `rebuild_cli_new.py` in the KENVUE folder is the reference implementation.
Copy and update `TARGET` path for each new week.
