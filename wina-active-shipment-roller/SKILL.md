---
name: wina-active-shipment-roller
description: Rolls over the active GWS shipments by filtering out Arrived or Cancelled shipments and updating the Shipment Report Date to the current date.
---

# wina-active-shipment-roller

This skill automatically rolls over the WINA GWS report for a new week. It uses a dual-load technique (loading both a data-only and a formula-preserved version of the workbook in memory) to accurately read calculated statuses like "Arrived" and "Cancelled", safely delete those rows, and update the Shipment report date of the remaining active rows to today's date—all without destroying any underlying Excel formulas.

## Usage
Run the script against the final output of the previous week's report to generate the starting base for the new week:
`ash
python scripts/rollover.py "path_to_excel_file.xlsx"
`
It will output a new file with _ROLLED.xlsx appended to the name.
