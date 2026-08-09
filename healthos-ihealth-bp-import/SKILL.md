---
name: healthos-ihealth-bp-import
description: >
  Imports blood pressure and pulse history from the iHealth KN-550BT cuff directly
  into the HealthOS bp_log.json on the PC, using ADB to pull SDK debug logs from
  the phone and decoding the raw BLE 0x4A historical data payload.
  Bypasses the broken iHealth OAuth API entirely. Use when the user asks to sync,
  pull, import, or update BP readings from their iHealth cuff or app into HealthOS.
---

# iHealth → HealthOS Blood Pressure Import Skill

## Overview

The iHealth MyVitals Pro app (`com.ihealthlabs.MyVitalsPro`) writes SDK debug logs
to the phone's external storage every time the KN-550BT cuff syncs over Bluetooth.
These logs contain raw BLE packets including the `0x4A` command — a historical BP
data dump from the cuff — decodable without any API tokens.

### Data Architecture

| File | Role |
|------|------|
| `data/blood_pressure_history.csv` | **Master** — source of truth, 87+ readings back to 2018 |
| `data/bp_log.json` | **Cache** — derived from CSV, auto-regenerated after every import, read by the HealthOS Flask server |
| `sync/bp_import.py` | **Pipeline script** — runs the full import + regen cycle |

Never edit `bp_log.json` directly. Always modify the CSV and re-run the pipeline.

---

## ADB Device Target Rules (CRITICAL)

| Device Name | Model | Connection | ADB Serial Target | Role |
| :--- | :--- | :--- | :--- | :--- |
| **S24 Ultra ("Biggest")** | `SM-S928U1` (Android 16) | Wi-Fi / mDNS | `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` | **Primary phone for iHealth & HealthOS sync** |
| **Note 9** | `SM-N960U1` (Android 10) | USB Cable | `2aaaf879c51c7ece` | Secondary test phone — **DO NOT USE FOR HEALTHOS** |

> ⚠️ **DISAMBIGUATION WARNING**: When multiple devices appear in `adb devices`:
> - ALWAYS use `-s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` for S24 Ultra / iHealth tasks.
> - NEVER use `2aaaf879c51c7ece` (Note 9) for HealthOS sync!

---

## Prerequisites

- ADB connected to phone over Wi-Fi (Wireless Debugging)
  - Target S24 Ultra: `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` (IP `192.168.4.83`)
  - Target string `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` auto-resolves active ports over mDNS—no manual port lookup needed.
  - ADB path: `C:\Users\whanusiewicz\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe`
- HealthOS directory: `C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\`
- SDK log dir: `C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\sync\ihealth_logs\`
  (stable — never changes between conversations; auto-created by `bp_import.py` on first run)

---

## Step-by-Step Workflow

### 1. Connect ADB

```powershell
$adb = "C:\Users\whanusiewicz\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
& $adb connect adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp
& $adb devices   # verify connection
```

If connection is refused, ask user to re-enable Wireless Debugging and provide the new port.
User can share a screenshot of the Wireless Debugging screen — read the IP:port from it.

---

### 2. Launch iHealth on S24 Ultra to Trigger Cuff Sync

```powershell
& $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell monkey -p com.ihealthlabs.MyVitalsPro -c android.intent.category.LAUNCHER 1
Start-Sleep -Seconds 35   # give the app time to find and sync the cuff
```

> Always launch the app before pulling logs so the KN-550BT cuff auto-connects over
> Bluetooth and flushes any new readings to the SDK debug log. **Wait at least 35 seconds** —
> the full sync cycle (scan → connect → handshake → download offline records) takes 15–20s
> minimum; 35s is safe.
>
> If the user confirms the cuff already synced manually, use `-SkipLaunch` but **still
> pull logs fresh** — the sync may have updated a log file after your last pull.
> Always re-pull today's hour file by name after the import and re-run if it grew
> (see §Log Pull Timing below).

---

### 3. Pull SDK Debug Logs (~7 days of history)

```powershell
$dest = "C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\sync\ihealth_logs"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$adb = "C:\Users\whanusiewicz\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"

# Step A: Explicitly pull today's active SDK log file by name pattern
$todayLog = (Get-Date -Format "yyyy-MM-dd")
& $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell "ls /sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/${todayLog}*.txt" | ForEach-Object {
    $file = $_.Trim()
    if ($file -and $file -notmatch "No such file") { & $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp pull $file "$dest\" }
}

# Step B: Bulk pull remaining history & verify gaps
& $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp pull /sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/ $dest

$phoneFiles = (& $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell ls /sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/) -split "`n" |
    ForEach-Object { $_.Trim() } | Where-Object { $_ -match "\.txt$" }
$localFiles = Get-ChildItem $dest -Filter "*.txt" | Select-Object -ExpandProperty Name
$missing = $phoneFiles | Where-Object { $_ -notin $localFiles }
foreach ($f in $missing) {
    Write-Host "Pulling missing file: $f"
    & $adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp pull "/sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/$f" "$dest\$f"
}
```

> **Why**: The iHealth app creates a new log file each hour (`YYYY-MM-DD-HH_SDK_Debug.txt`).
> A bulk `adb pull` may miss a file written during or just before the pull. Always verify
> the phone's live directory listing and pull any gaps individually.

---

### 4. Run the Pipeline Script

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"          # required alongside PYTHONIOENCODING on Python 3.12 / Windows 11
python "C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\sync\bp_import.py"
```

> **Important**: Set **both** `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1`. Either alone
> is insufficient on Windows 11 with Python 3.12 — the script will crash on the ⚠️
> and 🚨 emoji in the danger-zone output.

The script automatically:
- Reads all SDK logs from the scratch `ihealth_logs/` folder
- Extracts and decodes all `0x4A` BLE payloads
- Deduplicates against existing CSV entries
- Appends new readings with `Source` = `iHealth_KN550BT_BLE`
- Auto-populates `Note` with `⚠️ High` (SYS>160 or DIA>100) or `🚨 Crisis` (SYS≥180 or DIA≥110)
- Saves updated CSV (master)
- Regenerates `bp_log.json` (cache) from CSV

---

### 4. Verify Output

The script prints a summary:
```
[CSV] Loaded: 87 existing readings
[BLE]   3 new reading(s) from SDK logs
[OK]    CSV saved: 90 total readings
[OK]    bp_log.json regenerated: 90 entries
-------------------------------------------------------
  3 new reading(s) added to your log.
  Latest: Jul 17, 2026 @ 05:56
  BP:     161/94  Pulse: 71  ⚠️ High
  [!] 46 reading(s) above elevated threshold (SYS>160 or DIA>100)
-------------------------------------------------------
```

---

## BLE 0x4A Protocol Reference

**Payload format**: `[01 00] [N × 11-byte entries]`  
First 2 bytes = header (skip). Each 11-byte entry:

| Byte | Field | Formula |
|------|-------|---------|
| e[0] | year − 2000 | e.g. `0x1A` = 26 → 2026 |
| e[1] | month | 1–12 |
| e[2] | day | 1–31 |
| e[3] | hour | 0–23 |
| e[4] | minute | 0–59 |
| e[5] | flags/user slot | ignore |
| e[6] | systolic delta | `systolic = e[6] + e[7]` |
| e[7] | diastolic | dual-use: also low byte of systolic |
| e[8] | pulse | beats/min |
| e[9–10] | padding | ignore |

### Strict BLE Measurement Payload Validation Rules
1. **Require 0x4A / 0x8F Measurement Packet Signature:**
   - Do NOT decode handshake, battery, or status ACK packets (e.g. `0x20`, `0x21`, `0x40`, `A00F0020...`).
   - Only parse log lines containing explicit measurement payloads: `haveNewData(0x4A, ...)` or `0x8F` (143 decimal) / valid SYS byte ranges (`80–220`).
2. **Verify Offline Batch Transfer Completion:**
   - Wait until `stopDiscovery()` or `STATE_DISCONNECTED` is logged following an offline batch transfer to ensure all readings are flushed to `ihealth_sdk/*.txt` before executing `bp_import.py`.

**Verified against**: iHealth app UI on 2026-07-16, 2026-07-17, 2026-07-22, and 2026-07-24.
Cross-check at least one reading against the app's Trends tab after a new decode.

> ⚠️ **Bogus reading guard**: If any systolic value < 80 appears in the log, the
> decoder has a bug (e.g. wrong entry size or parsing connection handshake bytes). Do NOT let them accumulate — run a
> cleanup pass immediately:
> ```python
> # Remove rows where SYS < 80 from blood_pressure_history.csv, then re-run pipeline
> rows = [r for r in rows if int(r["SYS(mmHg)"]) >= 80]
> ```
> This happened on 2026-07-22 when a multi-size guessing decoder generated 27 phantom
> entries (systolic 60–74), and on 2026-07-24 when an ACK handshake packet was parsed. The fix is to lock entry_size=11 unconditionally and enforce the `0x4A` signature check.

---

## CSV Schema

```
Date,Time,SYS(mmHg),DIA(mmHg),Pulse(Beats/Min),Note,Source
"Jul 17, 2026",05:56,161,94,71,⚠️ High,iHealth_KN550BT_BLE
```

| Column | Notes |
|--------|-------|
| Date | `MMM D, YYYY` format (e.g. `Jul 7, 2026`, not `Jul 07, 2026`) |
| Time | `HH:MM` 24-hour |
| Note | Auto-filled: `⚠️ High` if SYS>160 or DIA>100; `🚨 Crisis` if SYS≥180 or DIA≥110 |
| Source | `iHealth_KN550BT_BLE` for cuff readings; `iHealth_export` for older app exports |

---

## Log Pull Timing

The iHealth SDK creates a new log file each hour (`YYYY-MM-DD-HH_SDK_Debug.txt`).
These files are **written in real-time while the app is running**. A reading taken
while the app is closed is stored on the cuff and downloaded the next time the app
opens and syncs — the `0x4A` payload appears in the log for **that sync session's
hour**, not the hour the reading was taken.

**Key consequence**: always pull SDK logs *after* the user confirms the iHealth app
has completed its sync. If unsure, pull → import → then pull today's file again by
exact name and compare byte counts. If it grew, re-run `bp_import.py`.

```powershell
# Re-pull today's file and check if it changed
$dest   = "C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\sync\ihealth_logs"
$today  = (Get-Date -Format "yyyy-MM-dd-HH")
$remote = "/sdcard/Android/data/com.ihealthlabs.MyVitalsPro/files/ihealth_sdk/${today}_SDK_Debug.txt"
$local  = "$dest\${today}_SDK_Debug.txt"
$before = if (Test-Path $local) { (Get-Item $local).Length } else { 0 }
& $adb pull $remote $local
$after  = (Get-Item $local).Length
if ($after -gt $before) {
    Write-Host "Log grew ($before → $after bytes) — re-running import..."
    & python $PIPELINE
}
```

---

## Important Notes

- **SDK logs only go back ~7 days** (daily rotation). For older history beyond that,
  use the iHealth app: **Account → Share Data → Blood Pressure → CSV**, then pull the
  exported file from `/sdcard/Download/` via ADB and merge manually.

- **iHealth OAuth API is broken**: `sync/ihealth.py` requires tokens in
  `data/ihealth_tokens.json` that are currently unavailable. Do NOT use it.
  This BLE log method is the active import path.

- **KN-550BT device info**:
  - MAC: `E0:62:34:F6:AF:6A` (app nickname: "Track")
  - App package: `com.ihealthlabs.MyVitalsPro`
  - App is not debuggable (`run-as` does not work — use external storage only)

- **HealthOS server** runs on `http://localhost:3000`. Start it with:
  ```powershell
  python server.py
  ```
  from `C:\Users\whanusiewicz\Desktop\MAIN\Around the House\HealthOS\`
  It reads `bp_log.json` for `/api/summary` and `/api/trends` endpoints.
