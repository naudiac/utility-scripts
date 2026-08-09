---
name: wina-air-report-update
description: Manages the daily Kenvue Air Shipment Report lifecycle including pipeline execution, Cesar review tracking, Kenvue version generation, email drafting, and workspace archiving. Use when the user says anything related to running the air report, processing Cesar's reply, producing the Kenvue version, archiving today's cycle, or showing corrections/tasks.
---

# WINA Air Report Update — Agent Skill

## Workspace Layout

All work happens under:

```
C:\Users\whanusiewicz\Documents\Cheryl Lee\Weekly Global Report - Air\WorkspaceOpsBravoMark3\
```

Full folder tree:

```
WorkspaceOpsBravoMark3/
│
├── pipeline_air.py              ← DATA INTEGRITY LAYER (internal enrichment)
├── generate_kenvue.py           ← CLIENT TRANSFORMATION LAYER (Kenvue output)
│
├── ACTIVE CONTRACTS/            ← Reference data: contract + auto-rating files
│
├── Inbox/
│   └── GWS/                    ← DROP ZONE: new GWS system export each day
│
├── Baseline/
│   └── current_baseline.xlsx   ← THE ONE LIVE BASELINE (always exactly 1 file)
│
├── Output/                     ← Pipeline iteration outputs
│   └── Global_Air_Template-WeekXX-DayY-N.xlsx
│
├── Cesar/
│   ├── Pending Review/         ← Copy of the file sent to Cesar today
│   ├── Returned/               ← DROP ZONE: manual .msg drop OR auto-saved from Outlook
│   ├── cesar_corrections.xlsx  ← PERMANENT corrections + directive log (never deleted)
│   └── daily_tasks.txt         ← Today's task list (resets each day, archived daily)
│
├── Kenvue/
│   ├── Ready/                  ← Kenvue-stripped file pending William's send
│   └── Sent/                   ← Archive of .xlsx files sent to Kenvue (by date)
│
└── Archive/
    ├── YYYY-MM-DD/             ← One dated folder per completed day
    │   ├── gws_export.xlsx
    │   ├── internal_vN.xlsx
    │   ├── cesar_returned.xlsx
    │   ├── cesar_email.msg
    │   ├── kenvue_sent.xlsx
    │   └── daily_tasks_completed.txt
    ├── _Review for Delete/     ← Dev/migration dump — William clears at his own pace
    └── _pre_production_old/    ← Bulk archive of pre-production old files
```

**Key invariants:**
- `Baseline/` always contains exactly **one** file: `current_baseline.xlsx`.
- `cesar_corrections.xlsx` is permanent — it is never deleted or overwritten, only appended to.
- The Kenvue version is a one-way client output — it is **never** used as a baseline.

---

## Daily Cycle

### 1. Overnight Baseline Resolution Gate (4 PM → 10 AM)

From **4 PM the prior day** through **10 AM today**, the skill monitors Outlook for any reply from `JCastro@witlogistics.com` to yesterday's chain.

```
Cesar replied before 10 AM?
  YES → log all changes and directives
        → his returned file becomes TODAY's current_baseline.xlsx
        → pipeline can run immediately
  NO  → prior day's v1 (the 8:30 AM internal send) becomes TODAY's baseline
        → pipeline runs at 10 AM (late start is acceptable)
```

At 8 AM William receives a status notification:
- `"Baseline resolved: Cesar's reply from [HH:MM]"` — or —
- `"No Cesar reply yet — using prior day v1 as baseline. Waiting until 10 AM."`

10 AM is the **hard deadline** for baseline commitment. After 10 AM, the pipeline runs regardless of whether Cesar has replied.

---

### 2. Pipeline Auto-Trigger Conditions + Manual Trigger

**Auto-trigger** when ALL of the following are true:
- Baseline is resolved (file present in `Baseline/`)
- GWS export is present in `Inbox/GWS/` (if absent: run with most recent file and flag as stale)

**Manual trigger:** William says any trigger phrase (see Trigger Vocabulary below). Manual trigger overrides auto-conditions.

**What the pipeline does each run:**
1. Reads `Baseline/current_baseline.xlsx`
2. Reads the latest file from `Inbox/GWS/` (or most recent if stale)
3. Reads `ACTIVE CONTRACTS/` for lane, TT, carrier, region lookups
4. Consults `Cesar/cesar_corrections.xlsx` — skips writing to any field with `Still Active = Yes`
5. Applies pattern-based learning suggestions (advisory only, printed in AAR — never auto-applied)
6. Outputs: `Output/Global_Air_Template-WeekXX-DayY-N.xlsx` (N auto-increments)

---

### 3. Pre-Send Manual Edit Detection (Hybrid Confirm)

Before creating the Cesar draft, the skill diffs the pipeline output against the file William is actually going to send.

If differences are found:
> "You changed these N cells since the pipeline ran — log them as protected manual corrections?"

William confirms → cells are logged to `cesar_corrections.xlsx` (Source: `William - Manual`) and become write-protected for future pipeline runs.

---

### 4. Cesar Draft Email Creation

Target: **8:30 AM**

- **To:** `JCastro@witlogistics.com`
- **CC:** Persists from the last iteration unless William explicitly changes it
- **Subject:** `GWS-AIR REPORT - MM/DD/YYYY`
- **Attachment:** Latest file from `Output/`
- **Action:** Outlook Draft created — William reviews and sends manually

William is notified: `"Draft ready for review — please send when ready."`
The sent file is copied to `Cesar/Pending Review/`.

---

### 5. Intra-Day Iteration Loop (8:30 AM → 4:00 PM)

The skill monitors Outlook for:
- **A) Cesar's reply** to the chain
- **B) Teammate replies** in the same chain

**On Cesar reply:**
- Type A — File edits only → diff vs. sent file → log corrections → promote to `Baseline/current_baseline.xlsx` → notify William
- Type B — Email directives only → parse email body → add to Directive Log (Tab 2 of `cesar_corrections.xlsx`) → add to `daily_tasks.txt` → notify William
- Type C — Both → do both

**On teammate reply:**
- Notify William: `"[Name] replied in the chain"`
- If they updated CargoWise per Cesar's directive: William re-runs the GWS desktop shortcut (see CargoWise Data Source below), drops the new export in `Inbox/GWS/`, then says "run next iteration" or the skill auto-detects the new file

**Each new iteration:**
- Pipeline re-runs against updated baseline + new GWS export
- New output file: suffix increments (-2, -3, -4...)
- New Cesar draft created
- William reviews and sends

---

### 6. 4 PM Hard Cutoff — Kenvue Version Generation

At 4 PM, `generate_kenvue.py` is called on the best available internal file:
1. Cesar's last returned/approved file (if he replied today)
2. Last vN sent to Cesar (if he replied but gave no final go-ahead)
3. v1 (if Cesar never replied at all today)

The Kenvue output is placed in `Kenvue/Ready/`.
An Outlook Draft is created for the Kenvue email.

---

### 7. Kenvue Review Checklist

William receives the following checklist with each Kenvue version:

```
✅ KENVUE VERSION READY — Week XX / MM/DD/YYYY
════════════════════════════════════════════════════
 [ ] SHIPMENT column removed
 [ ] OWNER column removed
 [ ] FRN column removed
 [ ] Internal colors normalized
 [ ] Iteration number dropped from filename
 [ ] Cesar corrections preserved in baseline
 [ ] William manual corrections preserved in baseline
 [ ] Cascade rules applied (blanks cleaned)
 [ ] Data integrity flags: N warnings (if any)
 [ ] Open directives: N tasks still outstanding
 [ ] CC list matches last iteration
 [ ] Email draft body reviewed

  ⚠️  [Any warnings surface here]
```

William sends the Kenvue email manually from Outlook Drafts.

---

### 8. End of Day — Baseline Lock

Tomorrow's baseline is always an **internal** file, never the Kenvue version:

| Situation | Tomorrow's Baseline |
|---|---|
| Cesar approved today | Cesar's returned file |
| Cesar replied, no final "go" | Last vN sent to Cesar |
| Cesar never replied | v1 (the 8:30 AM internal send) |

The skill prompts William to confirm the baseline selection if ambiguous.

---

### 9. Archive Trigger

Triggered by `"Archive today"` or an end-of-day auto-prompt.

- All day artifacts moved to `Archive/YYYY-MM-DD/`
- Working zones cleared: `Inbox/GWS/`, `Output/`, `Cesar/Pending Review/`, `Kenvue/Ready/`
- `Baseline/` and `cesar_corrections.xlsx` are **never touched** by archive
- `daily_tasks.txt`: completed items archived, file reset for tomorrow

---

## Trigger Vocabulary

| What you say | What happens |
|---|---|
| `"Run today's report"` | Manual pipeline trigger (overrides auto-conditions) |
| `"Run next iteration"` | Re-runs pipeline, increments version number |
| `"Process Cesar's reply"` | Manual trigger for Cesar return flow (auto also runs) |
| `"Produce Kenvue version"` | Calls `generate_kenvue.py` → `Kenvue/Ready/` → drafts Kenvue email |
| `"Archive today"` | Moves all day artifacts to `Archive/YYYY-MM-DD/` → clears working zones |
| `"Show Cesar's corrections"` | Summary from corrections log: recent changes, patterns, suggestions |
| `"Show today's tasks"` | Prints `daily_tasks.txt` with pending/done status |
| `"What's the baseline?"` | Shows `current_baseline.xlsx` filename, date, and last Cesar reply info |

---

## Cesar Reply Detection

**Hybrid auto-scan logic:**

1. **Manual .msg drop takes priority** — if a `.msg` file appears in `Cesar/Returned/`, process it immediately regardless of Outlook scan state.
2. **Auto-scan Outlook** — monitor for replies from `JCastro@witlogistics.com` in the active chain automatically.

**Detection parameters:**
- **Cesar's email:** `JCastro@witlogistics.com`
- **Subject pattern:** contains `GWS-AIR REPORT`

On detection, determine reply type (A/B/C) and route accordingly (see Intra-Day Iteration Loop above).

---

## Email Rules

- **ALL emails are Drafts only — nothing ever auto-sends.** William always sends manually from Outlook Drafts.
- **Kenvue email subject line format (canonical, confirmed with Craig Meehan 06/23/2026):**
  ```
  Daily Global Air Shipment Report - Week [#] - MM/DD/YYYY - Kenvue
  ```
  - Hyphens as separators — not commas, not slashes
  - Week number = ISO week number (e.g., 26)
  - Date = date the report covers
  - "Kenvue" always at end
  - **Hyphens are correct in the subject line.** The "no hyphens" rule applies only to conversational prose in the email body, never to the subject line format string.
- **CC list persists** from the last iteration unless William explicitly changes it.
- **Cesar draft subject:** `GWS-AIR REPORT - MM/DD/YYYY`

**Confirmed Kenvue recipients (To:):**

| Name | Email |
|---|---|
| Rohilla Shivani | SRohil01@kenvue.com |
| SMITH LORI | LSmith9@kenvue.com |
| Petrunyak Alexander | apetrun1@kenvue.com |
| Meehan Craig | CMeehan6@kenvue.com |

**Internal CC:**

| Name | Email |
|---|---|
| Jerry S. Mabasa | JMabasa@witlogistics.com |
| Cesar Castro | jcastro@witlogistics.com |
| Giorgio Laccona | GLaccona@witlogistics.com |
| Stephen Hui | SHui@witlogistics.com |

---

## Corrections Log: cesar_corrections.xlsx

This file is **permanent and ever-growing** — it is never deleted, reset, or overwritten. It is the full audit trail and pattern-learning source for the pipeline.

### Tab 1: Corrections Log

| Column | Description |
|---|---|
| Log Date | Date the correction was processed |
| HAWB | Shipment identifier |
| Field Name | Column header that was changed |
| Pipeline Value | What the pipeline had written |
| Corrected Value | What it was changed to |
| Source | `Cesar - File Edit` / `Cesar - Directive/William` / `William - Manual` |
| Still Active | `Yes` / `No` |
| Override Date | If pipeline later overrode the correction, the date |
| Override Reason | Why the override occurred (logical impossibility description) |
| Notes | Pattern notes accumulated over time |

### Tab 2: Directive + Task Log

| Column | Description |
|---|---|
| Date | When the directive was received |
| From | `Cesar` or teammate name |
| Email Subject | Chain reference |
| Directive Text | Exact instruction verbatim |
| Assigned To | `William` or teammate name |
| Task Type | `Data Update` / `Email Draft` / `Research` / `Other` |
| Status | `Pending` / `In Progress` / `Done` / `Waiting on Teammate` |
| Applied In Iteration | Which pipeline version number reflects the outcome |
| Completed Date | Date marked done |

### Source Priority (highest to lowest)

1. `Cesar - File Edit`
2. `Cesar - Directive/William`
3. `William - Manual`
4. Pipeline / GWS

---

## Pipeline Write-Protection Rules

### Protected Fields — Skip Writing

If `Still Active = Yes` exists for a given HAWB + Field Name combination in the Corrections Log:
- The pipeline keeps the corrected value as-is
- The GWS/pipeline-derived value is **not written**

### Override Allowed — Logical Impossibility Only

An override is permitted only when the corrected value is factually impossible given current data. Override always flags William in the AAR.

**Override conditions:**
- Actual delivery date is before Cesar's planned delivery date
- Status = "Arrived" but no ATA date exists
- Date field is >180 days old with no matching active shipment

**On override:**
- Set `Still Active = No` in the Corrections Log
- Log `Override Date` + `Override Reason`
- Add a warning to the pipeline AAR and quality audit section

### Learning Mode (Advisory Only — Never Auto-Applied)

If Cesar has corrected the same Field + Lane combination **3 or more times**, the AAR prints:

```
⚡ SUGGESTION: [Field] for [Lane] corrected by Cesar N times.
   GWS says [X]. Cesar typically sets [Y]. Review before sending.
```

This is a suggestion only. The pipeline never auto-applies it.

---

## generate_kenvue.py Rules

`generate_kenvue.py` is the **client transformation layer**. It is a separate script from `pipeline_air.py` and is **never called automatically**. It is called only:
- On explicit command from William (trigger: `"Produce Kenvue version"`)
- By the skill at 4 PM as part of the hard cutoff flow

**What it does:**

1. **Strip internal columns:** Removes `SHIPMENT`, `OWNER`, and `FRN` columns entirely
2. **Color normalization:** Removes all internal markup fill colors from cells — the Kenvue version has clean, neutral formatting
3. **Apply cascade validation rules** (run before column stripping):

   **Rule 1 — Scheduled TT block:**
   ```
   IF [Reason for scheduled TT not met Controllable/Uncontrollable] is blank:
     → blank [Scheduled TT not met Failure Code/Reason]
     → blank [Scheduled TT not met Comments]
   Note: Cesar's values remain intact in Baseline/ — only the Kenvue copy is cleaned.
   ```

   **Rule 2 — Main performance block:**
   ```
   IF [Controllable/Uncontrollable] is blank:
     → blank [Failure Code/Reason]
     → blank [Comments]
   ```

   **Rule 3 — Reverse integrity flag (warning only, no auto-fix):**
   ```
   IF child fields have values but parent field is blank:
     → Add to Kenvue checklist: "⚠️ [Field] has value but parent
       [Parent Field] is blank — review before sending"
   ```

4. **Filename:** Drop the iteration number from the output filename.
   - Input: `Global_Air_Template-WeekXX-DayY-3.xlsx`
   - Output: `Global_Air_Template-WeekXX-DayY.xlsx`

5. **Output location:** `Kenvue/Ready/`

**What it does NOT do:** Touch data logic, consult the corrections log, modify the baseline, or call `pipeline_air.py`.

---

## Baseline Rules

The baseline (`Baseline/current_baseline.xlsx`) is **always an internal full file**. The Kenvue version is **never** used as a baseline.

**Selection logic at end of day:**

| Situation | Baseline for Tomorrow |
|---|---|
| Cesar approved today | Cesar's returned file (from `Cesar/Returned/`) |
| Cesar replied but no final "go" | Last vN sent to Cesar (from `Output/`) |
| Cesar never replied | v1 — the 8:30 AM send (first `Output/` file of the day) |

**Overnight check:** Between 4 PM and 10 AM the following morning, monitor for a late Cesar reply before committing to the fallback baseline. If a late reply arrives before 10 AM, his returned file supersedes the fallback.

---

## Stale GWS Handling

If no new GWS export is present in `Inbox/GWS/` when the pipeline runs:
- Run the pipeline anyway using the **most recent** available GWS file
- Flag as **stale** prominently in the AAR:

```
⚠️  STALE GWS EXPORT — using [filename] from [date]. New GWS export was not found.
    Shipment coverage may be incomplete. Re-run with fresh export when available.
```

The report date displayed is the current date regardless of GWS file age.

---

## Schedule

| Time | Action |
|---|---|
| **8:00 AM** | Pipeline auto-runs if baseline resolved + GWS present; William notified of baseline status |
| **8:30 AM** | Cesar draft ready (target) |
| **10:00 AM** | Baseline resolution hard deadline — pipeline runs regardless of Cesar reply status |
| **4:00 PM** | Hard cutoff: `generate_kenvue.py` runs on best available file; Kenvue review checklist shown |
| **5:00 PM** | If Cesar never replied, Kenvue version is produced from v1 (if not already done at 4 PM) |

---

## CargoWise Data Source

The GWS system export is generated from CargoWise via a desktop shortcut.

| Parameter | Value |
|---|---|
| Report PK | `26c72c63-3de3-4b4c-9749-f7c0dd3a70ae` |
| Instance | `WLTJFK` |
| Domain | `wisecloud.zone` |

**Workflow when CargoWise is updated by a teammate (per Cesar's directive):**
1. Teammate updates CargoWise
2. William runs the desktop shortcut to generate a fresh GWS export
3. William drops the new `.xlsx` into `Inbox/GWS/`
4. William says `"Run next iteration"` — or the skill auto-detects the new file and triggers the pipeline

---

## After-Action Report (AAR) Format

Each pipeline run prints a console summary that is also copied to the Windows clipboard:

```
=== GWS Airfreight Automation - After-Action Report ===
Run Date/Time              : YYYY-MM-DD HH:MM
Output File                : Global_Air_Template-WeekXX-DayY-N.xlsx
Baseline Used              : current_baseline.xlsx
GWS Export                 : [filename] ([FRESH / ⚠️ STALE — dated YYYY-MM-DD])
New Shipments Added        : N
Protected Fields Skipped   : N
Override Warnings          : N
Rows Flagged (RED/YELLOW)  : N
Learning Suggestions       : N
=======================================================
[⚡ SUGGESTION lines if any]
[⚠️ OVERRIDE WARNING lines if any]
```
