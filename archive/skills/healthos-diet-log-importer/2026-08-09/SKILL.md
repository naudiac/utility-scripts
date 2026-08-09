---
name: healthos-diet-log-importer
description: >
  Imports and analyzes meal photos from William's phone 'Diet log' album (/sdcard/DCIM/Diet log),
  calculates macro & carbohydrate intake, estimates glycemic impact, and logs nutritional data into
  HealthOS/data/nutrition_log.json while updating health logs.
---

# HealthOS Diet Log & Vision Nutrition Importer

## Overview
Automates food and nutrition logging for William's HealthOS ecosystem. Scans the phone's dedicated **`Diet log`** album (`/sdcard/DCIM/Diet log`), pulls meal photos via ADB, extracts exact meal timestamps, performs multimodal vision analysis for ingredient identification, calculates macronutrient and carb totals, and updates `HealthOS/data/nutrition_log.json`.

---

- **Target Device & Album Path**: Samsung Galaxy S24 Ultra (`adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` / `192.168.4.83`)
> ⚠️ **ADB Target Selection**: Always target S24 Ultra via mDNS string `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp`. Do NOT target `2aaaf879c51c7ece` (Note 9).
- **Auto-Discovery Pipeline**: `sync_diet_album.py` uses `get_adb_device_and_folder()` to auto-discover active ADB devices and scan for folder candidate variations (`/sdcard/DCIM/Diet log`, `/sdcard/DCIM/1Diet log`, `/sdcard/Diet log`, etc.).
- **Core Rule**: Whenever William takes a photo or video and saves it to the `Diet log` album on his phone, it explicitly indicates **what he ate** and **when he ate it** (from file timestamp/metadata).

---

## Workflow Steps

### 1. Execute Album Sync Script
Run the automated diet album sync script:
```powershell
python "C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\sync_diet_album.py"
```

### 2. Vision Meal Analysis & Macro Calculation

> ✅ **Use the `local-image-viewer / view_local_image` MCP tool** to view meal photos in any session (CLI or IDE). This returns a proper MCP image content block — no binary crash, no file copying needed.

For each pulled meal photo in `scratch/diet_photos_temp/`:

1. Call `mcp local-image-viewer/view_local_image` with the full absolute path:
   ```
   path: "C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\scratch\diet_photos_temp\<filename>"
   ```
   The tool resizes the image to max 1600px and returns it as a multimodal vision attachment the model can see directly.

2. Identify all ingredients, cooking medium (e.g., olive oil, butter), and estimated portion sizes from the result.
3. Also incorporate any verbal meal corrections the user provided (e.g., "include 4 farm eggs and olive oil") — these override or supplement visual analysis.

4. Calculate detailed nutritional breakdown:
   - `calories` (kcal)
   - `protein_g` (g)
   - `fat_g` (g)
   - `carbs_g` (g) / `net_carbs_g` (g)
   - `fiber_g` (g), `sugar_g` (g), `sodium_mg` (mg)
   - **Glycemic Category**: Very Low (<10g net carbs) / Moderate / High Glycemic

### 3. Log Update & Journaling
1. Append structured entry to `HealthOS/data/nutrition_log.json`:
   ```json
   {
     "date": "YYYY-MM-DD",
     "meal_type": "lunch",
     "time": "HH:MM",
     "description": "Short description of meal",
     "calories": 520,
     "protein_g": 42.0,
     "fat_g": 34.0,
     "net_carbs_g": 8.0,
     "items": [ ... ],
     "notes": "Low-carb meal cooked in olive oil.",
     "source_photo": "IMG-20260802-WA0023.jpeg"
   }
   ```
2. Cross-reference `glucose_log.json` to link premeal/postmeal blood sugar readings with the exact food consumed.
3. Update `HealthOS/data/health_journal.json` and `healthos_master_record.md`.

### 4. Janitor Cleanup
Clean up local temporary pulled images from `scratch/diet_photos_temp/` after logging completes.
