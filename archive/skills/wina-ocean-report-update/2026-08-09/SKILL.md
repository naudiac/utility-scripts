---
name: wina-ocean-report-update
description: >-
  Manages the weekly WINA ocean GWS report lifecycle using two canonical
  pipelines: (1) db_intake_pipeline.py — queries CargoWise DB directly via the
  GlobalOceanWeekly reporting view, enriches new BOLs against active contracts,
  and injects them into the GWS; (2) apply_milestone_updates.py — fetches live
  actuals from CW via cw_data_fetcher.py and refreshes milestone dates,
  highlights, and comments for all active rows. Use when the user says anything
  like "run the ocean pipeline", "update the GWS", "inject new BOLs", or
  "refresh milestones".
---

# WINA Weekly Ocean Report Update

## ⚠️ Canonical Pipeline Architecture (confirmed 2026-08-06)

There are **two pipelines** with distinct, complementary roles. Do NOT mix them up.

| Pipeline | Script | Purpose | When to run |
|---|---|---|---|
| **Intake** | `2023/db_intake_pipeline.py` | Queries CW GlobalOceanWeekly DB view → finds new BOLs → enriches → injects into GWS | Weekly (when new GWS iteration needed) |
| **Milestone Refresh** | `WorkspaceOpsCharlieTest2/apply_milestone_updates.py` | Fetches live CW actuals → updates dates, highlights, AB comments on active rows | Daily / mid-week |

### Why db_intake_pipeline.py is the correct intake tool

`db_intake_pipeline.py` queries `wlk_fn_Report_GlobalOceanWeekly_20240528` — a pre-built
CW reporting view that includes **origin/dest city, service type, shipper, consignee,
country** — everything needed for contract fuzzy-matching and lane assignment.

`cw_data_fetcher.py` (used inside WorkspaceOpsCharlieTest2) queries raw CW tables
(`JobHeader` / `JobShipment`) which only return BOL + File# + dates — **no city,
no service type, no shipper**. It finds BOL IDs but cannot enrich them for lane
assignment. It is only useful for milestone date refreshes on existing rows.

> **Do NOT use `cw_data_fetcher.py` Query B output as a source for new BOL intake.**
> Its 161-row "new BOLs" result includes removed/excluded BOLs and has blank city
> data. `db_intake_pipeline.py` properly filters `removed.xlsx` and the existing GWS,
> yielding the true net-new count (e.g. 10 for W32).

## Folder Structure

```
CESAR File/
  2023/                          <- Weekly working folder
    db_intake_pipeline.py        <- PRIMARY intake script (Stage 1+2 combined)
    WINA_GWS Report_W##_YYYY-N.xlsx  <- Current GWS (input)
    WINA_GWS Report_W##_YYYY-N+1.xlsx <- Output after intake run
    removed.xlsx                 <- BOL exclusion list

  WorkspaceOpsCharlieTest2/      <- Milestone refresh workspace
    cw_data_fetcher.py           <- Fetches CW actuals for EXISTING active rows
    apply_milestone_updates.py   <- Updates milestone dates + highlights + comments
    clear_unnecessary_highlights.py <- Always run immediately after apply_milestone_updates
    ACTIVE CONTRACTS/            <- Contract files (never move)
    Output/Processing/           <- cw_data_fetcher writes cw_report2.xlsx here
    _run_config.json             <- Shared config (stage2_out, stage3_out, report2, etc.)
```

## Held-Shipment Case Tracking (`pending_reviews.json`)

When the pipeline flags a data conflict (city mismatch, missing report-2 data,
carrier conflict, etc.), the affected BOLs are tracked in `pending_reviews.json`.

### Workflow

1. **Pipeline flags issue** → case created with status `open`
2. **Email drafted** → questions prepared for team, timeline entry added
3. **Email sent** → status changes to `awaiting_response`
4. **Response received** → answers recorded in the questions array
5. **Resolved** → decision and code changes documented
6. **Processed** → BOLs corrected in the GWS, status set to `processed`

### Pipeline Integration

The pipeline checks `pending_reviews.json` on every run (step 15) and surfaces
any open cases in the console output — case ID, BOL count, days open, and
unanswered questions. Nothing falls through the cracks.

### Case Categories

| Category | When |
|---|---|
| `origin_city_mismatch` | System origin doesn't match contract |
| `dest_city_mismatch` | System destination doesn't match contract |
| `lane_id_conflict` | Lane assignment is unclear |
| `missing_report2_data` | BOL in report-1 but not in report-2 |
| `carrier_mismatch` | Carrier SCAC conflicts between sources |
| `contract_expired` | Lane matched to an expired contract |

### Updating a Case

When the team responds, update the case in `pending_reviews.json`:
- Fill in `answer`, `answered_by`, `answered_date` for each question
- Add a `response_received` entry to the timeline
- Change status to `response_received`
- After applying the fix, add `resolved` and `processed_into_report` timeline entries


## Canonical Weekly Workflow

> [!IMPORTANT]
> **ALWAYS run the pipelines one stage at a time. STOP after each and wait for
> explicit user approval before proceeding to the next.**

### Step 1 — Update db_intake_pipeline.py paths

At the top of `2023/db_intake_pipeline.py`, update two lines:

```python
GWS_TARGET = _CUR + r'\WINA_GWS Report_W##_YYYY-N.xlsx'    # current input file
GWS_OUTPUT = _CUR + r'\WINA_GWS Report_W##_YYYY-(N+1).xlsx'  # new output iteration
```

The iteration number (N) increments by 1 each run. **Always read the actual
current filename — do not assume it increments by exactly 1** (manual edits
may have bumped it further).

### Step 2 — Run intake pipeline

```
cd "CESAR File\2023"
python db_intake_pipeline.py
```

Runs in ~60-90 seconds (hits CW DB twice). After completion:
- New BOLs are injected directly into `GWS_OUTPUT`
- All fields enriched: Lane ID, Carrier, CTT, Sector, Region, container flags
- If `Found 0 new BOLs`: script copies input to output unchanged — still OK

### Stage Gate — After Intake

Present a summary table:
`BOL NO | Origin | Destination | Carrier | Lane ID | Equipment | CTT | Contracted`

Highlight any rows where `Contracted Lane = No` — these are spot shipments,
confirm handling before proceeding.

### Step 3 — Run CW milestone refresh (same session or separately)

```
cd "CESAR File\WorkspaceOpsCharlieTest2"
# Update _run_config.json: stage2_out = full path to the new GWS output file
python cw_data_fetcher.py --gws "<full path to GWS file>"
python apply_milestone_updates.py
python clear_unnecessary_highlights.py
```

`clear_unnecessary_highlights.py` **must always run immediately after**
`apply_milestone_updates.py` — never skip it.

### Step 4 — _run_config.json for milestone refresh

Before running `apply_milestone_updates.py`, ensure `_run_config.json` has:

```json
{
  "week": "##",
  "stage2_out": "<full path to the GWS file to update>",
  "stage3_out": "Output/WINA_GWS_W##_YYYY-N_stage3.xlsx",
  "report2": "Output/Processing/cw_report2.xlsx"
}
```

`stage2_out` is the **input GWS** for milestone updates (the file `cw_data_fetcher`
read and `apply_milestone_updates` will update). `stage3_out` is the output.

- `current_iter` = the number in the GWS filename
- `output_iter`  = current_iter + 1
- `gws_input`    = exact filename from Intake/
- `stage2_out`   = `Output/WINA_GWS_W{week}_{year}-{output_iter}_stage2.xlsx`
- `today`        = today's date (YYYY-MM-DD)

The iteration may jump by more than 1 if manual edits were made outside the pipeline
between runs. **Always read the actual Intake filename — do not assume it increments by 1.**

## Workflow the Agent Should Follow

> [!IMPORTANT]
> **ALWAYS run the pipeline one stage at a time. STOP after each stage and wait for
> explicit user approval before proceeding to the next. Never chain stages together.**

### Stage Gate — After Stage 1
Present a summary table with columns:
`BOL NO | Origin | Destination | Carrier | Lane ID | Equipment | Status (OK / UNMATCHED)`

Highlight any UNMATCHED rows separately and confirm handling before running Stage 2.

### Stage Gate — After Stage 2
Confirm: rows appended, output filename, row range written (e.g. "rows 1309–1322").
Ask explicit permission before any further processing.

When the user says they have a new weekly report to process, follow these steps:

### 1. Check Intake Folder
Verify `Intake/` contains exactly:
- `current report-1.xlsx`
- `current report-2.xlsx`
- `WINA_GWS Report_W##_YYYY-#.xlsx`

If any are missing, ask the user to provide them before proceeding.

### 2. Check for New Contracts
Ask: *"Have any contract files changed since last week?"*  
If yes, copy the new contract to `ACTIVE CONTRACTS/` and update the
`KNV_CONTRACT` or `JNJ_CONTRACT` constant in `pipeline_stage1.py`.
The pipeline auto-detects the corrupted lane column name in newer Kenvue contracts.

### 3. Back Up Before Running
Run `python backup_pre_stage2.py` to snapshot all files to Google Drive before
making any changes.

### 4. Run the Pipeline
```
python pipeline_stage1.py
```

### 5. Check for REVIEW_REQUIRED File
After running, **always check `Output/` for a `REVIEW_REQUIRED_*.xlsx` file.**
If one exists, open it and bring each flagged issue to the user for a decision
before finalising the output. Common issues include:
- A system-exported city name that doesn't match the contract city
- A BOL assigned to a lane whose contract shows a different destination

Do NOT auto-correct review flags without user confirmation. Update `CITY_FIXES`
in `pipeline_stage1.py` only after the user has confirmed the correct mapping.

### 6. Validate Output
Open `Output/current report-1-W##-enriched.xlsx` and verify:
- All rows have LANE ID (or `CONTRACTED LANE = No` for uncontracted)
- CARRIER / LINER is a 4-letter SCAC on every row — never blank
- Exactly one container flag = 1 per row; others = 0
- REGION OF OWNERSHIP filled for all rows
- City names match contract spelling — no ALL-CAPS raw system values
- Date columns show dates with no green error triangles (proper Excel date objects)

### 7. Update GWS File Reference for Next Week
At the top of `pipeline_stage1.py`, update `INTAKE_GWS` to match the new
GWS filename that will be in Intake next week.

## Key Business Rules (Do Not Change Without Confirmation)

- **Container flags**: Exactly one of the three container columns = 1 per row; others = 0.
- **Carrier**: Always a 4-letter SCAC. First try MASTERBILL prefix; fallback to GWS history for that origin-dest pair. Never leave blank.
- **CONTRACTED LANE**: `Yes` only if a Lane ID was successfully matched. `No` if uncontracted.
- **REGION OF OWNERSHIP**:
  - Taken directly from the contract where explicitly stated.
  - Fallback rule: `EMEA` if Europe-origin → Africa or Middle East destination; `NA` for all other combinations.
  - Note: "NA" is North America in this context — pandas `keep_default_na=False` must always be used when reading contracts to prevent "NA" being parsed as NaN.
- **City spellings**: Always use the exact spelling from the active contract, not the raw system export value.
  - Cities from `CITY_FIXES` must be applied **before** fuzzy matching, not after, so the normalization actually influences the lane lookup.
- **Date format**: All date columns must be native Excel Date objects formatted as `d-mmm-yy`. Never write dates as plain text strings.
- **Output formatting**: Every output file must have freeze panes on row 1, AutoFilter on all columns, and column widths auto-fitted to content.

### Spot Shipment Rule (No Contract Lane Match)

When Stage 1 produces a shipment with no matched Lane ID (`CONTRACTED LANE = No`):

| Field | Value |
|---|---|
| LANE ID | blank (leave empty) |
| CONTRACTED LANE | No |
| CONTRACT TRANSIT TIME | Scheduled transit time (days) − 2 |

- Include the shipment in the output as-is — do NOT exclude it.
- Proxy for scheduled TT at Stage 1 time: use `(LAST_ETA − LEG_1_ETD)` from report-2,
  then subtract 2 days.

### Container Type Verification Protocol (40GP vs 40HC vs 20FT)

* **Verification Sources (CargoWise DB or `current report-2.xlsx`)**: Always match intake shipments from `current report-1` against `current report-2.xlsx` (`CONT_CODE`) or query the live CargoWise read-replica SQL Server DB directly (`JobHeader` / `JobShipment` / `JobContainer` / `RefContainer`) by `HOUSEBILL`, `MASTERBILL`, or `File #` (`SHIP_ID`) to determine the exact container type code:
  - `20GP` / `20ST` → `NO. OF 20 FT` = 1, `40 GP` = 0, `NO. OF 40 / 40HC` = 0
  - `40GP` / `40ST` / `40DV` → `NO. OF 20 FT` = 0, `40 GP` = 1, `NO. OF 40 / 40HC` = 0
  - `40HC` / `40HQ` / `40RF` → `NO. OF 20 FT` = 0, `40 GP` = 0, `NO. OF 40 / 40HC` = 1
* **Numeric Cell Formatting**: Always write explicit numeric integer values (`1` and `0`) into container count columns. Never leave them as empty/blank strings or dropped dtypes.


### New Shipment Intake Filtering Protocol

To identify new shipments to add from `current report-1.xlsx`:
1. Extract all BOLs from `2023/current report-1.xlsx`.
2. Filter out BOLs present in active `GWS Report template`.
3. Filter out BOLs listed in `removed.xlsx` / `purged_bols.json` (2,636 removed BOLs).
4. Filter out Sector M (Taiwan / Intra-Asia non-Kenvue) shipments.
5. Enrich remaining new shipments against `ACTIVE CONTRACTS/` and save to `current_report_1_WXX_ready_for_injection.xlsx` for user review.

- Do NOT flag spot shipments for review — they are expected and pass through silently.
- `CONTRACTED LANE` = `No` on every spot shipment — no exceptions.

## EDD / EXP Service Rule

Some shipments have `SVC_LVL = EDD` (Express Door-to-Door) in report-2. These must be handled specially:

1. **Detect**: Check `SVC_LVL` column in report-2 for `EDD`.
2. **Present as DTD**: Set `SERVICE TYPE = DTD` in the output — never show EDD externally.
3. **Use EXP lane**: Do NOT use the standard DTD lane. Instead, look up the correct EXP lane from:
   `ACTIVE CONTRACTS/Ocean AutoRating Org list.xlsx` — most recent data sheet (first non-admin tab).
   Rows with `(EXP)` in the Lane Name column are the express service lanes.
4. **Lane ID by container**: Read the 20GP, 40GP, or 40HC column from the EXP row to get the correct lane ID.
5. **Transit time**: Use the T/T (Days) from the EXP row — it will differ from the standard lane TT.

**AutoRating file structure:**
- Row 1 (0-indexed) = real column headers
- Lane Name format: `OriginCityCC>Dest City, ST (EXP)` — strip `(EXP)` and split on `>` to get cities
- City codes: trailing 2-char country code must be stripped (e.g., `MagoulaGR` → `Magoula`)
- Lane ID cells may contain merged-cell bleed-over — always extract with regex `[A-Z]{2,4}\d{3,4}`

**Current EXP routes (as of 2026-May 1b sheet):**

| Route | 40GP Lane | 40HC Lane | TT |
|---|---|---|---|
| Magoula → Lebanon, PA | KONA1987 | KONA1993 | 26 days |
| Magoula → Mooresville, IN | KONA1988 | KONA1994 | 29 days |
| Magoula → Palmetto, GA | KONA1989 | KONA1995 | 28 days |

> When a new version of the AutoRating file is provided, copy it to `ACTIVE CONTRACTS/Ocean AutoRating Org list.xlsx`
> (overwrite). The pipeline always reads the first non-admin sheet automatically.

### EDD Carrier Conflict Detection

When a shipment has `SVC_LVL = EDD` and is assigned to an EXP lane, **always verify
the actual carrier** before assuming the expected EXP carrier applies.

**Source of truth hierarchy (most → least authoritative):**
1. CargoWise DB: `JobConsol.JK_OA_ShippingLineAddress` → resolve via `OrgAddress.OA_CompanyNameOverride`
2. Master Bill prefix from report-2 (first 4 chars of `MASTERBILL` = SCAC code)
3. Expected carrier from contract / AutoRating file

**If the actual carrier (from MBL/CW) differs from the expected EXP carrier for that lane:**
- **Do NOT change the carrier** — the actual booking takes precedence over the rate expectation
- **Treat the shipment as normal** for all data fields (lane, TT, sector, region)
- **Flag the conflict** in the GWS output after Stage 2:
  - Write to the `Comments` column:
    `"EDD SERVICE FLAG: Shipment recorded as EDD in CargoWise but booked on [CARRIER] (MBL: [MASTERBILL]), not [EXPECTED_CARRIER] as expected for EXP [ROUTE] lanes per Cesar's guidance. Treated as standard [CARRIER] shipment. Verify with Cesar."`
  - Highlight the `BOL NO` cell: **yellow fill** (`FFFF00`) + **bold orange text** (`CC6600`)

> **Cesar's standing note (confirmed 2026-07-07):** For Greece→US, expedited service
> (EXP) uses ONE Line; regular service uses MSC. This is the general arrangement —
> individual bookings may deviate. Always verify via the actual CW booking record.

## Updating City Fix Mappings

If you encounter a new raw city name that isn't being corrected, add it to the
`CITY_FIXES` dictionary in `master_update.py`:

```python
CITY_FIXES = {
    'RAW SYSTEM VALUE': 'Contract Spelling, State/Province',
    ...
}
```

Always verify the correct spelling against the active contract before adding.

> **Known system artifact**: The raw system export may output `CHICAGO` as a
> destination for some Gdansk-origin lanes. This is confirmed to be an artifact;
> the correct destination per contract (KONA1657) is `Mooresville, IN`.
> This mapping is already in `CITY_FIXES`.

## Common Mistakes

1. **Files not in Intake/** — the pipeline reads exclusively from `Intake/`.
   Dropping files in the root folder will not work.
2. **"NA" parsed as NaN** — always use `keep_default_na=False, na_values=['']`
   when reading any contract file with pandas. Region of Ownership = "NA" is
   valid data, not missing data.
3. **File open in Excel** — the script cannot save while the output file
   is open. Close it before running, then reopen after.
4. **Ignoring REVIEW_REQUIRED** — always check Output/ for a review file
   after each run. Flag issues must be confirmed with the user before finalising.
5. **Kenvue contract lane column** — newer versions of `Contract528957-2.xls`
   may have a corrupted lane ID column name (e.g. `Lane IDs/Item IDsLCL0656`).
   The pipeline detects this automatically — no manual fix needed.

## Script Location

All processing scripts live in the root of the working folder:
- `pipeline_stage1.py` — main weekly Stage 1 script (use this)
- `pipeline_stage2.py` — Stage 2: updates the GWS report with new rows + date rules
- `backup_pre_stage2.py` — pre-run Google Drive backup
- `backup_skill_to_drive.py` — skill file backup to Drive

Do not move or rename them. All paths are relative to the folder they sit in.

---

## Stage 2 — GWS Report Update

Stage 2 takes the enriched Stage 1 output and writes the new BOLs into the weekly
GWS Excel report. Run **after** Stage 1 has completed and the enriched file is in `Output/`.

### Quick Start

```
python pipeline_stage2.py
```

Output is written to `Output/WINA_GWS_W##_stage2_test.xlsx`. Review before
promoting to the final filename.

### What Stage 2 Does

| Step | Action |
|---|---|
| 1 | Updates `Shipment report date` to today for all rows where `Shipment Status` ≠ ARRIVED and ≠ CANCELLED |
| 2 | Appends new BOLs by copying the last existing row (template), then overwriting all fields |
| 3 | Fills each new row from Stage 1 output + report-2 (see field map below) |
| 4 | Applies date rules for `PLANNED DELIVERY TO DOOR DATE`, `ORIGINAL ETA DATE`, `ORIGINAL ETD DATE`, `ATD Date` |
| 5 | Applies formatting (freeze panes, AutoFilter, column widths) |

### Field Map for New Rows

**From Stage 1 output (contract / lane data):**

| GWS Column | Stage 1 Field |
|---|---|
| BOL NO | BOL NO |
| Provider | PROVIDER |
| Region of ownership | REGION OF OWNERSHIP |
| Contracted Lane | CONTRACTED LANE |
| Lane ID | LANE ID |
| Service type | SERVICE TYPE |
| Incoterm | INCO |
| Carrier/Liner | CARRIER / LINER |
| Shipper Name | SHIPPER NAME |
| Consignee Name | CONSIGNEE NAME |
| Sector | SECTOR |
| Origin Region | ORIGIN REGION |
| Destination Region | DESTINATION REGION |
| Origin Country | ORIGIN COUNTRY |
| Origin city | ORIGIN CITY |
| Dest Country | DEST COUNTRY |
| Dest City | DEST CITY |
| No. of 20 ft | NO. OF 20 FT |
| No. of 40ft | 40 GP |
| No. of 40HC | NO. OF 40 / 40HC |
| Contract transit time | CONTRACT TRANSIT TIME |

**From report-2 (HOUSEBILL lookup):**

| GWS Column | report-2 Field |
|---|---|
| File # | SHIP_ID |
| Owner | USER_NAME (if "AUTOMATED DATA IMPORT" → "NEED OWNER") |
| Container No. | CONT_NUM |
| No. of Units (Pallets/Packages) | PACKS |
| UOM | PACKS_TYPE |
| Total CMB | ACT_VOL |
| Total Weight in KG | ACT_WGT |
| Container Type | CONT_CODE |
| Empty pick-up Date | EMPTY_OUT_GOU_CY |
| PLANNED PICK UP DATE | ACT_PICKUP |
| Actual Pick up Date | ACT_PICKUP |
| Gate In Date | FULL_IN_GIN_CTO |
| ATA Date | LAST_ATA |
| Discharge Date | FULL_UNLOAD_FUL_CTO |
| FRN | FRN_DATE |
| Gate Out Date | FULL_OUT_GOU_CTO |
| Requested delivery to door date | DLV_REQD_BY |
| Actual delivery to door date | ACT_DELIVERY |
| Empty return Date | EMPTY_IN_GIN_CY |

**Always set to fixed values:**
- `Invoice Number` → `NOT AVAILABLE`
- `No. of 45ft / 45HC / 53ft` → `0`
- `Column #` → continues from last existing Column # (last existing + 1, 2, …)
- `Shipment report date` → today's date

### Date Logic

#### ORIGINAL ETD DATE / ATD Date
- If `LEG_1_ATD` ≤ today in report-2: set **both** `ORIGINAL ETD DATE` and `ATD Date` = `LEG_1_ATD`
- Else if `LEG_1_ETD` exists: set `ORIGINAL ETD DATE` = `LEG_1_ETD`, clear `ATD Date`
- Else: clear `ATD Date` only

#### Contracted DTD (CONTRACTED LANE = Yes, Service = DTD)
Anchor = `ACT_PICKUP` from report-2 (= what is written to `PLANNED PICK UP DATE`)

```
PLANNED DELIVERY TO DOOR DATE = ACT_PICKUP + CTT + 2
ORIGINAL ETA DATE             = PLANNED DELIVERY TO DOOR DATE − lead_time
```

> ATD drives `ORIGINAL ETD DATE` / `ATD Date` only — it does NOT change the
> anchor for `PLANNED DELIVERY TO DOOR DATE`.

#### Non-contracted DTD (CONTRACTED LANE = No, Service = DTD)
```
ORIGINAL ETA DATE             = LAST_ETA from report-2
PLANNED DELIVERY TO DOOR DATE = LAST_ETA + lead_time
Contract transit time         = (PLANNED DELIVERY − ACT_PICKUP) − 2
```

#### Contracted PTD / non-DTD (Service ≠ DTD)
```
Anchor                        = LEG_1_ETD from report-2
PLANNED DELIVERY TO DOOR DATE = LEG_1_ETD + CTT + 2
ORIGINAL ETA DATE             = PLANNED DELIVERY − lead_time
```

#### Lead Time Rules

| Destination | Lead time (days) |
|---|---|
| Lebanon, PA | 7 |
| Fontana, CA | 7 |
| Port Jervis, NY | 8 |
| Memphis, TN (Taiwan origin) | 8 |
| Memphis, TN (all other origins) | 5 |
| Albuquerque, NM | 14 |
| EMEA destinations (Region of Ownership = EMEA) | 4 |
| All other US / CA | 5 |

### Untouchable Columns (Never Write to These)
- `Shipment Status` — formula; write-protecting by not including in field map
- `Lane Name` — customer-created formula
- `Scheduled transit time` — formula
- `Schedule vs Contract TT` — formula
- `Dest. Port to Planned delivery (Days)` — formula

### Column # Sequence Rule
The `Column #` column uses a 1-based integer counter starting from row 2.
Last existing value in the base GWS = `max_row − 1`.
New rows continue: `max_row, max_row+1, ..., max_row+n−1`.
Always rendered in **red font** (`FF0000`).

### File Path Constants (top of pipeline_stage2.py)

```python
GWS_BASE   = 'Intake/WINA_GWS Report_W##_YYYY-4.xlsx'   # previous-week GWS
GWS_TARGET = 'Intake/WINA_GWS Report_W##_YYYY-6.xlsx'   # comparison target (dev only)
STAGE1_OUT = 'Output/current report-1-W##-enriched.xlsx'
REPORT2    = 'Processed/current report-2.xlsx'
OUTPUT     = 'Output/WINA_GWS_W##_stage2_test.xlsx'
TODAY      = datetime(YYYY, MM, DD)   # update to current processing date each week
```

Update `GWS_BASE`, `STAGE1_OUT`, `OUTPUT`, and `TODAY` each week before running.

---

## Stage 3 — Email Updates & Milestone Management

After Stage 2, process any carrier/forwarder email updates and refresh all active
shipment milestones from the latest report-2 export.

### Scripts

| Script | Purpose |
|---|---|
| `apply_milestone_updates.py` | Refresh actuals + Revised dates for all active rows from report-2; update AB comments; apply highlight and color rules |
| `clear_unnecessary_highlights.py` | Remove yellow highlights from milestone cells where condition is no longer met |
| `apply_email_update.py` | One-off script — update a single Revised milestone field from an email |

### Email Update Workflow

When a carrier/forwarder email arrives with a revised milestone date:

1. **Identify the File # (SHIP_ID)** from the email (e.g. `S00237750`)
2. **Look up the BOL** in the GWS by File # column (D)
3. **Cross-check report-2**: confirm the system has been updated with the same date
   - If report-2 matches → proceed
   - If report-2 does not match → do NOT update GWS yet; wait for system to be updated first
4. **Write to the correct Revised column** (see Revised column rules below)
5. **`ORIGINAL` columns are frozen** — never change them after Stage 2 is complete

### Active Shipment Milestone Refresh

Run `apply_milestone_updates.py` to pull the latest data from report-2 for all active rows:
- Updates blank actual milestone fields from report-2 (never overwrites existing values)
- Updates Revised milestone columns with the 3-way logic (see below)
- Updates `Comments` column (AB) with missing milestone label (pipe-separated)

Run `clear_unnecessary_highlights.py` immediately after to remove stale yellow highlights.

### Revised Milestone Column Rules

There are 4 Revised columns: `Revised planned pick up date` (AW), `Revised ETD Date` (BB),
`Revised ETA date` (BE), `Revised planned delivery to door date` (BO).

| State | Rule |
|---|---|
| Actual confirmed AND matches Original | **Clear Revised** (blank) — original was correct |
| Actual confirmed AND differs from Original | **Revised = Actual** — reflects where it ended up |
| Actual not yet confirmed | **Revised = latest estimate from report-2** (only if different from original) |

### Milestone Highlighting Logic

A milestone cell is highlighted **yellow** (`FFFFFF00`) when it needs attention:

| Cell | Highlighted when |
|---|---|
| `PLANNED PICK UP DATE` | Date ≤ today AND `Actual Pick up Date` blank |
| `Actual Pick up Date` | Same as above (both flagged together) |
| `Gate In Date` | Actual pickup confirmed AND gate-in still blank |
| `ORIGINAL ETD DATE` | Effective ETD ≤ today AND `ATD Date` blank |
| `ATD Date` | Effective ETD ≤ today AND ATD blank |
| `ORIGINAL ETA DATE` | ATD confirmed AND effective ETA ≤ today AND `ATA Date` blank |
| `ATA Date` | Same as above |
| `Discharge Date` | ATA confirmed AND discharge blank |
| `Gate Out Date` | Discharge confirmed AND gate-out blank |
| `PLANNED DELIVERY TO DOOR DATE` | Effective delivery ≤ today AND actual delivery blank |
| `Actual delivery to door date` | Same as above |

> **Effective date** = Revised date if it exists, otherwise Original date.

### Comments Column (AB — `Comments `) & In-Transit Delay (BJ)

Two columns work together to surface missing milestones:

**AB (`Comments `)** — format: `[free-form note] | Need ATA or Revised ETA date`
- Left of `|`: user-written, never overwritten
- Right of `|`: auto-generated — shows only the **next critical missing milestone** in sequence
- Cleared when all critical milestones are resolved; left side always preserved

#### AB Label Rules (Critical — Do Not Change Without Confirmation)

The label to the right of `|` is determined by the **first** milestone group where the
effective planned date < TODAY and the actual is blank:

| Scenario | Label |
|---|---|
| Milestone has its own **Revised date** (plan was updated) AND no actual yet | `Need Updated Revised ETA date` *(or the relevant rev col name)* |
| Milestone has **no Revised date** (only Original) AND no actual yet | `Need ATA or Revised ETA date` *(or the relevant label + rev col)* |

Full label examples by milestone:

| Milestone | No Revised date → label | Revised date exists → label |
|---|---|---|
| Pickup | `Need Actual Pick up Date or Revised planned pick up date` | `Need Updated Revised planned pick up date` |
| ATD | `Need ATD or Revised ETD Date` | `Need Updated Revised ETD Date` |
| ATA | `Need ATA or Revised ETA date` | `Need Updated Revised ETA date` |
| Delivery | `Need Actual Delivery or Revised planned delivery to door date` | `Need Updated Revised planned delivery to door date` |

> **Key rule:** the word "Revised" is intentionally **not** used when there is no revised
> date — the label uses the milestone's short label (ATA, ATD, etc.) plus the revised
> column name as the "or" option. Only use "Need Updated" when a revised date actually
> exists in the cell.

#### ARRIVED Row Handling for AB Comments

- **ARRIVED + reason in col Z**: skip entirely — already categorised, leave untouched.
- **ARRIVED + no reason in col Z**: run the same AB comment logic as active rows.
  If a revised date exists but is past with no actual → `Need Updated Revised ETA date`.
  If no revised date → `Need ATA or Revised ETA date`.
  These must be resolved — an ARRIVED shipment with an unexplained No or unmet milestone
  cannot be left without a reason.
- **BJ (In-Transit Delay) column**: only updated for ACTIVE rows; ARRIVED rows are skipped.

**Critical milestones** (flagged in AB — require direct human follow-up):

| Milestone | Action required |
|---|---|
| Actual Pickup | Follow up with shipper/trucker — risk of missing vessel |
| ATD | Chase carrier for confirmed departure |
| ATA | Vessel arrived but unconfirmed — inland delivery cannot be planned |
| Actual Delivery | Past due, customer not confirmed received |

**BJ (`Reason for In-Transit delay (Internal data)`)** — format: `Missing: ATD, ATA, Discharge Date`
- Auto-generated full ordered list of **all** missing milestones (critical + operational)
- Operational milestones (Gate In Date, Discharge Date, Gate Out Date) appear here only
- Cleared automatically when all milestones are resolved
- Only cleared if existing content starts with `Missing:` (preserves any manual notes)

### Responsible Party Color Rules

Every highlight and text color is assigned based on which party is responsible:

| Origin / Rule | Fill color | Text color |
|---|---|---|
| Asia (`ASIA`, `CN`, `KR`, `TH`, `TW`, `VN`) | 🔴 Red `FF0000` | 🔴 Red `FF0000` |
| Europe (`EUROPE`, `AT`) | 🟡 Yellow `FFFF00` | 🟡 Gold `FFC000` |
| America (responsibility = `america`, or Greece) | 🔵 Sky-blue `00B0F0` | 🔵 Dark-blue `0070C0` |
| N/A / blank / NO. AMERICA | 🔵 Sky-blue | 🔵 Dark-blue |

#### Greek Shipment Rule (Critical)

Greece-origin shipments route **all** responsibility to America (blue), regardless of
which milestone triggered. Detection uses **BOL prefix**, not just the Origin Region
column (which stores `'EUROPE'` for Greek routes, not `'GR'`):

| BOL prefix | Origin Region | Treated as |
|---|---|---|
| `WINAES…` | any | 🔵 America (Greek office — always) |
| `WINAKE…` | `EUROPE` | 🔵 America (Greek route leg) |
| `WINAKE…` | `ASIA` | 🔴 Asia (Asian cargo, not Greek) |
| Other | `GR` | 🔵 America |

This is controlled by `GREEK_BOL_PREFIXES` and `GREEK_WINAKE_EUROPE` constants in
`apply_milestone_updates.py`. Do not change without user confirmation.

#### YES/NO Performance Columns (System 1)

Columns Z, AA, AB, AC (and CD–CG) receive the responsible-party fill based on:
- First `No` or `Not Met` value found scanning left-to-right through the YES/NO columns
- Fill color applied to Z, AA, AB (Comments), AC (BOL NO)
- If col Z already has a value (Controllable/Uncontrollable filled) → clear all fills
  (already categorised)
- For **current/recent week** ARRIVED rows with no Z reason: apply the No/Z/AA/AB/AC
  highlight rules — cannot leave an arrived shipment with an unexplained No

### Date Formatting Rule

All dates written programmatically must use Excel number format **`DD-MMM-YY`**
(e.g., `07-Jun-26` not `7-Jun-26`). This matches the existing GWS cell style.

### Actual Milestone Field Map (report-2 → GWS)

| GWS Column | report-2 Field | Rule |
|---|---|---|
| Actual Pick up Date | ACT_PICKUP | Fill blank only |
| Gate In Date | FULL_IN_GIN_CTO | Fill blank only |
| ATD Date | LEG_1_ATD | Fill blank only; only if ≤ today |
| ATA Date | LAST_ATA | Fill blank only |
| Discharge Date | FULL_UNLOAD_FUL_CTO | Fill blank only |
| FRN | FRN_DATE | Fill blank only |
| Gate Out Date | FULL_OUT_GOU_CTO | Fill blank only |
| Actual delivery to door date | ACT_DELIVERY | Fill blank only |
| Empty return Date | EMPTY_IN_GIN_CY | Fill blank only |

> **Safety rule**: Actual milestone dates already in the GWS are never overwritten —
> they may have been manually corrected. Only fill blank cells.

### Revised Milestone Field Map (report-2 → GWS, when actual not yet confirmed)

| GWS Column | report-2 Field |
|---|---|
| Revised ETD Date (BB) | LEG_1_ETD |
| Revised ETA date (BE) | LAST_ETA |
| Revised planned delivery to door date (BO) | EST_DELIVERY |
