---
name: wina-delay-notification
description: >-
  Generates the WINA ocean shipment delay notification email and saves it as an
  Outlook draft addressed to Justin Pippen and Chris Kim. Supports two modes:
  (1) Manual — user provides a list of BOL numbers; (2) Auto-scan — script
  reads the latest GWS Stage 2 Excel file and flags all BOLs where the
  Revised ETA is later than the Original ETA, the shipment is not yet delivered,
  and the status is not ARRIVED or CANCELLED. Use when the user says anything
  like "delay notification", "delay list", "put together the delays", or
  "create the delay draft".
---

# WINA Ocean Delay Notification

## Overview

This skill generates the weekly/ad hoc delay notification email for Kenvue
ocean shipments. It reads the latest GWS Stage 2 report, compiles delayed
BOLs into a formatted table, and creates an **Outlook draft** pre-addressed
to `Pippen, Justin` and `Kim, Chris`.

**Script:** `generate_delay_notification.py` (workspace root)  
**Source:** `Output/WINA_GWS_W##_*stage2*.xlsx` (latest file, auto-detected)  
**Recipients:** `Pippen, Justin`; `Kim, Chris`  
**Subject format:** `Delay Notification - MM/DD/YYYY`

---

## Two Operating Modes

### Mode 1 — Manual (user provides BOL list)

Use when the user pastes or types a list of BOL numbers.

```powershell
cd "path\to\WorkspaceOpsCharlieTest2"
python generate_delay_notification.py --bols "BOL1,BOL2,BOL3,..."
```

- Deduplicate the list before passing (remove exact duplicates; preserve order)
- BOLs not found in the GWS are noted in the email body and flagged to the user

### Mode 2 — Auto-scan (script finds delays automatically)

Use when the user says "scan for delays" or doesn't provide a list.

```powershell
python generate_delay_notification.py
```

**A BOL qualifies as delayed (auto-scan) when ALL of the following are true:**
1. `Revised ETA date` > `ORIGINAL ETA DATE` (confirmed carrier delay)
2. `Shipment Status` ≠ `ARRIVED` and ≠ `CANCELLED`
3. `Actual delivery to door date` is blank (still an open concern)

> This pattern was derived from the first manually-provided delay list
> (07/08/2026 — 52 BOLs, 50 found in GWS, all matched the above criteria).

---

## Columns in the Notification Table

| Column | GWS Source Field |
|---|---|
| BOL NO | BOL NO |
| Origin | Origin city |
| Destination | Dest City |
| Carrier | Carrier/Liner |
| Orig. ETD | ORIGINAL ETD DATE |
| Actual/ATD | ATD Date |
| Orig. ETA | ORIGINAL ETA DATE |
| Revised ETA | Revised ETA date |
| Days Delayed | Revised ETA − Original ETA (calculated) |
| Planned Delivery | PLANNED DELIVERY TO DOOR DATE |
| Revised Delivery | Revised planned delivery to door date |

---

## Workflow the Agent Should Follow

### 1. Receive the request

User says: "put together the delay notification list" (with or without BOLs).

### 2. Deduplicate BOLs (if manual mode)

If the user provides a BOL list, remove duplicates before running.  
Keep first occurrence; preserve order. Tell the user how many were removed.

### 3. Run the script

```powershell
cd "c:\Users\whanusiewicz\Documents\Cheryl Lee\Weekly Global Report - Ocean\CESAR File\WorkspaceOpsCharlieTest2"
python generate_delay_notification.py --bols "BOL1,BOL2,..."
# or for auto-scan:
python generate_delay_notification.py
```

### 4. Review output

Check the console output for:
- Number of shipments included
- Any BOLs NOT found in GWS — surface these to the user
- Whether any already-delivered BOLs appear (Actual delivery ≠ blank) — these
  are excluded from auto-scan but may be included in manual mode

### 5. Confirm draft

Tell the user:
- Draft created: subject, recipient count, shipment count
- Any warnings (missing BOLs, encoding issues with special chars)
- Ask if they want to adjust any columns or add/remove BOLs before sending

---

## Notes & Known Behaviors

- **Encoding**: The `—` (em dash) character may display as `â€"` in Outlook
  plain-text mode on some systems. If reported, replace with a plain `-`.
- **2 BOLs consistently missing**: `WINAKE26009277` and `WINAKE26009272` were
  not found in the GWS on the first run (07/08/2026). Confirm with user whether
  these should be added manually or skipped.
- **Auto-detect GWS**: The script finds the latest `*stage2*.xlsx` in `Output/`
  by modification time — no manual path update needed.
- **Column widths**: The table auto-sizes to content. Long city names may be
  truncated in the column header but not in the data rows.

---

## Script Location

```
WorkspaceOpsCharlieTest2/
  generate_delay_notification.py   ← main script (do not move)
```

## Preview-Only Mode (no Outlook draft)

```powershell
python generate_delay_notification.py --no-outlook --bols "BOL1,BOL2"
```

Use this to review the table in chat before committing to a draft.
