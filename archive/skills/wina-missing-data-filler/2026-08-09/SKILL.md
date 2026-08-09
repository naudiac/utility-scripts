---
name: wina-missing-data-filler
description: Fills missing data in the weekly WINA GWS report by fetching from CargoWise and updating highlights/milestone statuses.
---

# WINA Missing Data Filler

This skill takes a GWS report template and fills in missing values for key fields (Owner, Invoice Number, Container No., etc.) by querying the CargoWise database. It harmonizes ETA/ETD with actuals, identifies genuinely overdue milestones, updates cell highlighting (yellow for overdue), logs missing milestones to MILESTONE STATUS, and correctly colors the BOL NO text based on the origin/destination routing teams.

## Usage
Trigger this skill when the user asks to "fill missing data" on a GWS report, "update GWS with CargoWise", or "harmonize and format the GWS missing milestones".

1. Ensure you have the path to the active GWS Excel file.
2. Execute the python script:
   ``powershell
   python C:\Users\whanusiewicz\.gemini\config\skills\wina-missing-data-filler\scripts\fill_missing_data.py "C:\path\to\WINA_GWS_Report.xlsx"
   ``
3. The script will output a file with _UPDATED.xlsx appended to the name.

## Business Logic Handled
- **Invoice Number Variations**: Any null, blank, or 'NOT AVAILABLE' variations are overwritten explicitly with NOT AVAILABLE if no valid value exists in CargoWise.
- **Tighter Highlights**: Only critical milestones and container info (e.g. ATD, ATA, Container No) are highlighted yellow when overdue. Non-critical missing fields (e.g. FRN) are left un-highlighted.
- **Team Routing Colors**: The BOL NO is colored Black (complete), Red (Asia), Blue (North America), or Orange (EMEA).
