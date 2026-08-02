# OneTouch Reveal Multi-Agent History Extraction & Reconciliation

## Overview
This document outlines the multi-agent architecture and execution pattern used to harvest full blood sugar logbook histories directly from the Android **OneTouch Reveal** app (`com.lifescan.reveal`) over ADB and perform automated 100% data reconciliation against local HealthOS records (`glucose_log.json`).

## Architecture & Workflow

### 1. Agent 1: OneTouch UI Navigator & Data Harvester
- **Role**: Remote Android app interaction and screen parsing.
- **Methodology**:
  - Connects to the Samsung S24 Ultra via ADB (`192.168.4.83`).
  - Launches `com.lifescan.reveal` (`monkey -p com.lifescan.reveal -c android.intent.category.LAUNCHER 1`).
  - Executes vertical scroll swipes (`input swipe 500 1800 500 800`).
  - Captures Accessibility UI hierarchy dumps (`uiautomator dump /sdcard/onetouch_dump.xml` -> `pull`).
  - Parses date headers, timestamps, and `mg/dL` glucose values across all scroll viewports.
  - Outputs a deduplicated dataset to `scratch/onetouch_extracted.json`.

### 2. Agent 2: Glucose Log Auditor & Reconciler
- **Role**: Data integrity check and anomaly detection in `glucose_log.json`.
- **Methodology**:
  - Audits all logged records for timestamp formatting inconsistencies (e.g., ISO microsecond strings).
  - Identifies rapid retest pairs (<15 minute deltas) and potential BLE sync error overrides.
  - Constructs a baseline table of existing local records.

### 3. Reconciliation & Deduplication Engine
- Cross-references extracted app history `(timestamp, value)` pairs against local log entries.
- Eliminates duplicate entries while preserving 100% verified historical readings.

### 4. Automated Janitor Cleanup Protocol
- **Phone Storage Cleanup**: Deletes all temporary `/sdcard/*.png`, `/sdcard/onetouch_dump*.xml`, and `/sdcard/dump*.xml` files.
- **App Termination**: Issues `am force-stop com.lifescan.reveal` so the app is closed and not left running on the phone screen.
- **Local Workspace Cleanup**: Purges local scratch XML dumps, temporary `.json` extractions, and `.py` reconciliation scripts.

## Key Audit Results (August 2, 2026)
- **App Extractions**: 43 raw screen nodes -> 40 unique historical readings.
- **HealthOS Baseline**: 41 entries.
- **Cross-Match Accuracy**: **40 / 40 (100%)** match rate.
- **Pruned Artifact**: Removed 1 microsecond-format duplicate entry (`2026-07-21T15:19:15.673254`).
