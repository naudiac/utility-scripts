# HealthOS Cell Phone Diet Log & Vision Nutrition Importer

## Overview
This document outlines the architecture and execution model for William's **Diet Log Album Sync & Vision Nutrition Engine**, which imports meal photos from his Samsung Galaxy S24 Ultra (`Biggest`), extracts precise meal timestamps, calculates macronutrient and carb intake, and logs structured nutrition data into `HealthOS/data/nutrition_log.json`.

## Core Principle
- **Dedicated Phone Album**: `/sdcard/DCIM/Diet log` on phone (`192.168.4.83`).
- **Implicit Intent & Timestamping**: Taking a photo or video and placing it in the **Diet log** album on the phone explicitly defines **what was eaten** and **when it was eaten** (from image creation timestamp / EXIF data).

## Workflow & Pipeline

```
[ Phone: /sdcard/DCIM/Diet log ]
              │
      ADB Sync Script (sync_diet_album.py)
              │
              ▼
[ Local Temp Pull (scratch/diet_photos_temp/) ]
              │
     Multimodal Vision Analysis (view_file)
              │
              ▼
  • Ingredient Identification
  • Portion & Cooking Medium Estimation
  • Macronutrients (Calories, Protein, Fat, Carbs, Net Carbs, Fiber, Sodium)
  • Glycemic Impact Rating
              │
              ▼
[ HealthOS /data/nutrition_log.json & glucose_log.json Correlation ]
              │
              ▼
       Janitor Cleanup (Purge local temp files)
```

## System Implementation
- **Sync Script**: `HealthOS/sync_diet_album.py`
- **Agent Skill**: `healthos-diet-log-importer` (`~/.gemini/config/skills/healthos-diet-log-importer/SKILL.md`)
- **Data Stores**: `HealthOS/data/nutrition_log.json`, `HealthOS/data/glucose_log.json`, `HealthOS/data/health_journal.json`

## Real-World Validation (August 2, 2026)
- **Target Image**: `IMG-20260802-WA0023.jpeg` (Timestamp: `2026-08-02 13:44`)
- **Vision Extraction**: Detected sautéed green peppers, onions, and whole cremini/portobello mushrooms cooking in a stove pan.
- **Nutritional Output**: Correlated with 14:31 lunch entry (Steak + Sautéed Veggies, 8.0g net carbs, low glycemic impact).
