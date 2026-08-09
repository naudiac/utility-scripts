---
name: healthos-onetouch-bs-import
description: Imports blood sugar readings from OneTouch Verio Reflect meters over PC Bluetooth LE directly into HealthOS glucose_log.json. Trigger when the user asks to sync, pull, or read blood sugar or glucose from their meter directly on the PC.
---

# OneTouch Verio Reflect - PC Bluetooth LE Direct Sync

## Overview
Connects directly to William's OneTouch Verio Reflect glucose meters over Bluetooth LE on the PC, decodes the latest readings from the GATT notification stream, and appends them to `HealthOS/data/glucose_log.json`.

## Device & GATT Specifications
- **Target Device**: `1JM-US-TBA3961A` (`44:6F:F8:43:D7:3A`)
- **Service UUID**: `2dd10010-1c37-452d-8979-d1b4a787d0a4`
- **Write Characteristic (RX)**: `2dd10011-1c37-452d-8979-d1b4a787d0a4`
- **Notify Characteristic (NT)**: `2dd10013-1c37-452d-8979-d1b4a787d0a4`

## Protocol & Command Framing
1. Commands are sent as ASCII strings with MSB bit set (`b | 0x80`):
   - Read Patient Records: `RPR\r` (`0xD2 0xD0 0xD2 0x8D`)
   - Read Meter Records: `RMR\r` (`0xD2 0xCD 0xD2 0x8D`)
   - Dump Records: `DMP\r` (`0xC4 0xCD 0xD0 0x8D`)
2. Notification Stream Decoding:
   - **Method 1 (ASCII Digits)**: Strip MSB (`b & 0x7F`) and extract numbers between 40 and 500 mg/dL.
   - **Method 2 (LifeScan Hex Nibbles - 8-bit & 16-bit)**:
     - Map characters in `@`..`O` to nibbles `0..15` (`ord(c) - ord('@')`).
     - **8-bit paired nibbles**: `val = (n0 << 4) | n1` (e.g., `'J'+'J'` = `0xAA` = **170 mg/dL**).
     - **16-bit 4-nibble big-endian integers**: `val16 = (n0 << 12) | (n1 << 8) | (n2 << 4) | n3` (e.g., `'@'+'@'+'L'+'F'` = `0x00C5` = **197 mg/dL**).

## Execution Methods

### Mandatory Workflow: OneTouch Reveal Android ADB Extraction Pipeline

Do not use the direct PC BLE script (onetouch_ble.py) as it is highly unreliable. ALWAYS use the ADB extraction pipeline to pull readings directly from the phone app's UI on the S24 Ultra ("Biggest").

> ⚠️ **ADB Target Selection**: Always target S24 Ultra via mDNS string `$device = "adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp"`. Do NOT target `2aaaf879c51c7ece` (Note 9).

1. **Launch OneTouch Reveal App over ADB:**
   ```powershell
   $adb = "C:\Users\whanusiewicz\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
   $device = "adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp"
   & $adb connect $device
   & $adb -s $device shell monkey -p com.lifescan.reveal -c android.intent.category.LAUNCHER 1
   Start-Sleep -Seconds 30  # CRITICAL: 15s is often not enough. Give the app 30 seconds to connect to the meter over Bluetooth and fully sync.
   ```

2. **Dump & Parse Screen Hierarchy (`uiautomator dump`):**
   Always use `-s $device` to prevent "more than one device/emulator" errors.
   ```powershell
   & $adb -s $device shell uiautomator dump /sdcard/onetouch_dump.xml
   & $adb -s $device pull /sdcard/onetouch_dump.xml ./onetouch_dump.xml
   
   # Parse all visible glucose readings from the screen dump:
   [xml]$xml = Get-Content -Raw "./onetouch_dump.xml"
   $nodes = $xml.SelectNodes("//node[@text]")
   for($i=0; $i -lt $nodes.Count; $i++) { 
       if($nodes[$i].text -eq "mg/dL" -and $i -ge 1 -and $i -lt $nodes.Count-1) { 
           Write-Host "Found Reading: $($nodes[$i-1].text) mg/dL at $($nodes[$i+1].text)" 
       } 
   }
   ```
   - **Verification**: If the script output looks wrong or the newest reading isn't showing, the PowerShell parsing logic might have mismatched due to UI layout changes (like "Mentor Tips" boxes). In that case, manually `view_file` the XML dump to verify.
   - **Retry**: If the dump still shows the *old* reading, the meter hasn't synced yet. Wait another 20 seconds and run the dump again.
    - **Reconciliation Workflow**: Read `data/glucose_log.json` and find the most recent reading. Look at the extracted readings from the XML dump and locate that exact match. Any readings that appear *before* it in the UI list are new readings that haven't been logged yet.
     - Append the new readings to `data/glucose_log.json` with source `OneTouch Verio Reflect (ADB Screen Extraction)`.
     - Update `data/health_journal.json` and `healthos_master_record.md`.

### Meal Indicator Icons (Right-Side of Each Reading Card)

**CONFIRMED XML FINDING**: The `iv_meal_status` node always has empty `content-desc` and `text`. The `tv_value` node always ends with `U+00A0` (non-breaking space) regardless of meal type. **There is NO meal type data in the XML dump whatsoever.** Do not waste time searching for it.

Determine meal type using this process:

1. **Use the android-adb MCP `screenshot` tool** — this is the ONLY reliable method:
   ```
   mcp tool: android-adb / screenshot
   arguments: { "deviceId": "192.168.4.83:39909" }
   ```
2. **Read the meal icon visually from the MCP tool's inline image result.** That's it — you're done.
3. **HARD STOP — after the MCP screenshot call:**
   - Do NOT copy any file
   - Do NOT call `view_file`, `Read()`, or `Bash(Copy-Item...)` on any PNG path
   - Do NOT pull a screenshot via `adb shell screencap`
   - The MCP tool result is self-contained and complete
4. **Final fallback** — if the MCP tool fails or errors, log `"random"` and move on immediately.

| Icon visible in MCP screenshot | `type` to log |
|-------------------------------|--------------|
| 🍎 Whole apple (filled, dark) | `premeal` |
| 🍏 Apple core (eaten) | `postmeal` |
| No icon visible | `random` |

| `content-desc` value | `type` to log |
|----------------------|--------------|
| `"Before Meal"` or `"Fasting"` | `premeal` |
| `"After Meal"` | `postmeal` |
| `"No Tag"` or absent | `random` |

| Icon | Visual Description | Meaning | `type` Value |
|------|-------------------|---------|-------------|
| 🍎 | **Whole apple** (filled, dark) | Before Meal | `premeal` |
| 🍏 | **Apple core** (eaten, just core remains) | After Meal | `postmeal` |
| *(none)* | No icon | No meal tag | `random` |

### Multi-Agent Parallel Harvesting & Full History Reconciliation

When asked to audit or reconcile the full app logbook history against `glucose_log.json`, use a multi-agent parallel approach:

1. **Agent 1 (OneTouch UI Navigator & Data Harvester)**:
   - Connects to phone via ADB (`192.168.4.83`).
   - Launches `com.lifescan.reveal`.
   - Performs vertical scroll swipes (`input swipe 500 1800 500 800`) and captures UI dumps (`uiautomator dump /sdcard/dump.xml`).
   - Extracts all visible date headers, timestamps, and mg/dL values into a clean deduplicated JSON array saved to `scratch/onetouch_extracted.json`.

2. **Agent 2 (Glucose Log Auditor & Reconciler)**:
   - Concurrently audits `glucose_log.json`.
   - Identifies candidate duplicate timestamps (e.g. microsecond format artifacts or rapid retests), timestamp format anomalies, and source field variations.

3. **Reconciliation Engine**:
   - Cross-matches unique app history readings `(timestamp, value)` against `glucose_log.json`.
   - Flags missing entries to append or duplicate entries to prune.
   - Ensures 100% data integrity across mobile app history and HealthOS records.

### 🧹 Automated Janitor & Cleanup Protocol

ALWAYS execute the janitor cleanup step immediately after extraction and reconciliation complete to prevent leaving leftover app screenshots, XML dumps, or keeping the app active in foreground:

1. **Clean Phone Storage (`/sdcard/`)**:
   ```powershell
   & $adb -s $device shell rm -f /sdcard/onetouch_dump*.xml /sdcard/dump*.xml /sdcard/*.png /sdcard/DCIM/Screenshots/onetouch*
   ```

2. **Force-Stop OneTouch App**:
   ```powershell
   & $adb -s $device shell am force-stop com.lifescan.reveal
   ```

3. **Clean Local Temp/Scratch Files**:
   ```powershell
   Remove-Item -Path "./onetouch_dump*.xml", "./onetouch_extracted.json", "./reconcile.py" -Force -ErrorAction SilentlyContinue
   ```

