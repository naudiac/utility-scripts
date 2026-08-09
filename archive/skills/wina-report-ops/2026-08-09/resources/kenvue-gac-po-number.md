# Ability #1 — Kenvue GAC Report: PO Number → Extra Field 1 (Column BZ)

## Context

**Requested by:** Shivani Rohilla (Kenvue), email dated June 30, 2026  
**Subject:** "Require PO Number in GAC new template report"  
**Report:** Daily Global Air Shipment Report (GAC) — new template  
**Client:** Kenvue (JOHJOHCLE / `92DD86AF-E130-458C-9E34-2C4A0FEF1B36`)

Shivani's request:
> "In the new template, the PO Number must be mapped to 'Extra Field 1' (Column BZ). For reference,
> this information is captured under the column 'Kenvue_Ref_Numbers' in the old template Walker report."

---

## What "PO Number" Means Here

The data source is the existing CW SQL table-valued function:

```
OdysseyWLTJFK_UserRepository.dbo.wlk_ctfn_JobShipmentReferenceListAsStringWithRemovedList_20250523
```

This function takes a Shipment Job PK (`JS_PK`) and a separator, and returns all order/job
reference numbers for that shipment as a single comma-separated string (with noise references
filtered out). It is the same function that powers `Kenvue_Ref_Numbers` in the monthly Kenvue
Airfreight Report.

---

## Join Key

Each row in the output file corresponds to one **House BOL / consignment**.

- **Column in file:** `HAWB` (House Air Waybill number)
- **DB lookup:** `cvw_ShipmentForwarding.JS_HouseBill = '<HAWB>'`
- **Target PK:** `cvw_ShipmentForwarding.JS_PK`

Fallback join key (if HAWB is blank): `ShipmentID` = `cvw_ShipmentForwarding.JS_UniqueConsignRef`

---

## SQL to Run Per Row

```sql
SELECT 
    OdysseyWLTJFK_UserRepository.dbo.wlk_ctfn_JobShipmentReferenceListAsStringWithRemovedList_20250523(
        JS_PK, ','
    ) AS PO_Number
FROM cvw_ShipmentForwarding
WHERE JS_HouseBill = '<HAWB_VALUE_HERE>'
```

Or as a single-pass batch for the whole file (preferred — fewer round trips):

```sql
SELECT 
    cvw_ShipmentForwarding.JS_HouseBill AS HAWB,
    OdysseyWLTJFK_UserRepository.dbo.wlk_ctfn_JobShipmentReferenceListAsStringWithRemovedList_20250523(
        cvw_ShipmentForwarding.JS_PK, ','
    ) AS PO_Number
FROM cvw_ShipmentForwarding
WHERE cvw_ShipmentForwarding.JS_HouseBill IN (<COMMA_SEPARATED_HAWB_LIST>)
```

---

## Target Column

- **Column header label:** `Extra Field 1`
- **Always locate by header name** — never by column letter. The column letter differs
  between file versions:
  - **Kenvue's received file (stripped):** Column BZ — this is the reference Shivani uses
    because she sees the version with SHIPMENT, OWNER, and FRN removed.
  - **Our internal working file:** Column CC (or wherever it lands after internal columns
    shift it right). The fill script must find the column by matching the header label
    `Extra Field 1`, not by hardcoded letter.
- **Action:** Write the `PO_Number` string from the DB query result into the matched column
  for each row. Leave blank (do not error) if the DB returns NULL or empty.

---

## Execution Steps

1. User points to the output `.xlsx` file path.
2. Open the file with openpyxl. Scan the header row for a cell whose value is exactly
   `Extra Field 1` — record that column index. Also record the `HAWB` column index.
   **Never hardcode a column letter** — the position shifts between internal and Kenvue versions.
3. Collect all HAWB values from data rows (skip blanks). Build unique list.
4. Run the **batch** SQL query below against the CW DB using `query_cw.py` — one call for all HAWBs.
5. Build a lookup dict: `{ HAWB: PO_Number }`.
6. For each data row, look up the row's HAWB in the dict and write the PO_Number into the
   `Extra Field 1` column. Leave blank (do not error) if the DB returns NULL or empty string.
7. Save the file in place.
8. Report: rows filled / rows blank in DB / rows with no DB match at all.

### Verified column positions (as of 2026-07-07)

| File version | `Extra Field 1` letter | `HAWB` letter |
|---|---|---|
| Internal (our working file, 125 cols) | **CC** (index 81) | **AA** (index 27) |
| Kenvue received (stripped of SHIPMENT/OWNER/FRN) | **BZ** | shifts left |

This confirms why Shivani references "Column BZ" — she sees the stripped version.
The header-name lookup handles both versions automatically.

---

## Notes & Known Considerations

- This was implemented as an **ad hoc fill** while the pipeline is being revised. Once the pipeline
  is updated, this column should be added directly to the SQL stored procedure
  `wlk_fn_Report_Kenvue_Global_Air_20251217` and the new template file, making the ad hoc fill
  unnecessary.
- The SQL stored procedure change would be:
  ```sql
  ,OdysseyWLTJFK_UserRepository.dbo.wlk_ctfn_JobShipmentReferenceListAsStringWithRemovedList_20250523(
      cvw_ShipmentForwarding.JS_PK, ','
  ) AS Kenvue_Ref_Numbers
  ```
  And the template would need a corresponding `Extra Field 1` column mapping.
- **Last verified working: July 7, 2026** — production run on `Global_Air_Template-Week28-Day1-1.xlsx`.
  232 HAWBs queried in one batch; 99 rows filled, 129 blank in CW (normal), 4 unmatched.
- Originally researched in conversation `299928bd-7dd3-4937-ad16-5555c2c74869`
