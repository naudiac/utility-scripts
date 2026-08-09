---
name: wina-report-ops
description: >
  Ad hoc report fill operations for any client report. Use when the user asks to fill, populate,
  or update a specific column or field in an output report file (xlsx, csv, etc.) using data pulled
  live from the CargoWise database or another source. Covers all clients and report types.
  Current abilities: Kenvue GAC report — PO Number → Extra Field 1 (Column BZ).
---

# WINA Report Ops — Ad Hoc Fill Catalog

This skill is a growing catalog of ad hoc report fill abilities. Each ability is documented in
its own file under `resources/`. When the user triggers a fill, read the relevant resource file
for exact instructions and SQL.

---

## Prerequisites (All Fills)

- **VPN must be active** — the CargoWise DB requires a whitelisted IP. Always verify or remind
  the user before attempting any DB query.
- **CargoWise DB query tool**: Use the skill at
  `C:\Users\whanusiewicz\.gemini\config\skills\cargowise-database-query\scripts\query_cw.py`
- **File write**: You will need write access to the output `.xlsx` file the user points you to.
  Use `openpyxl` (or pandas) via a scratch Python script to write values.

---

## Catalog of Abilities

| # | Client | Report | Fill Target | Source | Resource File |
|---|--------|--------|-------------|--------|---------------|
| 1 | Kenvue | GAC New Template | Extra Field 1 (Column BZ) = PO Number | CW DB via `wlk_ctfn_...` function | [kenvue-gac-po-number.md](resources/kenvue-gac-po-number.md) |

> More abilities will be added here as they are defined. When adding a new ability, create a
> resource file in `resources/` and add a row to this table.

---

## How to Execute a Fill

1. Identify which ability matches the user's request (use the Catalog table above).
2. Read the corresponding resource file for exact SQL, join key, and target column details.
3. Ask the user to confirm the file path if they haven't provided it.
4. Verify VPN is active (attempt a simple DB query; if it fails, stop and ask user to connect VPN).
5. Run the fill script — read each row's join key, query DB, write result to target column.
6. Save the file and confirm completion to the user.
