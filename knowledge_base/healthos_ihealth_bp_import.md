# HealthOS iHealth KN-550BT Blood Pressure Import & Dynamic Dashboard Architecture

## Overview
This document defines the direct Bluetooth SDK log import pipeline and live dashboard recommendation architecture for William's **iHealth KN-550BT Blood Pressure Cuff** in HealthOS.

## Core Direct Bluetooth Log Sourcing
- **App Target**: iHealth MyVitals Pro (`com.ihealthlabs.MyVitalsPro`)
- **ADB Endpoint**: Wireless Debugging over Wi-Fi (`192.168.4.83:<port>`)
- **Phone Path**: `/sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/`
- **Data Protocol**: `0x4A` BLE offline data transfer payload containing year, month, day, hour, minute, pulse pressure delta, diastolic, and pulse.

## Resilient Daily SDK Log Sourcing Protocol
To ensure live cuff syncs are never missed due to bulk pull wildcards:
1. **Explicit Daily File Pull**: Always query and pull today's specific log pattern (`YYYY-MM-DD-HH_SDK_Debug.txt`) explicitly by filename.
2. **Bulk Pull & Gap Audit**: Execute bulk pull and cross-reference phone directory file count against local scratch.
3. **BLE Decoder Validation**: Enforce `0x4A` signature checks to prevent phantom ACK/handshake packet entries.

## Dynamic HealthOS Dashboard Architecture
- **Script**: `HealthOS/generate_health_summary.py`
- **Master Data**: `HealthOS/data/blood_pressure_history.csv`
- **Cache Data**: `HealthOS/data/bp_log.json`
- **Dynamic Feedback**: Recommendations dynamically evaluate latest `systolic`, `diastolic`, and `pulse` to categorize readings (Optimal, Normal, Elevated, High, Crisis) without relying on hardcoded static strings.
