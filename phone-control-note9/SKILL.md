---
name: phone-control-note9
description: >
  Control William's secondary Android phone (Samsung Galaxy Note 9) remotely
  from the PC via ADB. Use when the user asks to perform actions, test code,
  or run ADB commands on the Note 9.
---

# Samsung Galaxy Note 9 Control Skill

## Overview

This skill is for controlling and debugging William's secondary/test Android phone.

* **Phone:** Galaxy Note 9 (SM-N960U1)
* **Android:** 10 (SDK 29)
* **Connection Type:** Direct USB connection

---

## ADB Device Identification Matrix (CRITICAL)

| Device Name | Model | Connection | ADB Target Serial | Primary Role |
| :--- | :--- | :--- | :--- | :--- |
| **Galaxy Note 9** | `SM-N960U1` | USB Cable | `2aaaf879c51c7ece` | **Secondary test phone ONLY** |
| **S24 Ultra ("Biggest")** | `SM-S928U1` | Wi-Fi Wireless Debugging | `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` | Primary phone: HealthOS, BP, Diet, SMS |
| **Galaxy Watch5 Pro** | `SM-R920` | Wi-Fi Wireless Debugging | `adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp` | Smartwatch ONLY |

---

## Target Selection & Disambiguation

When executing ADB commands, the Galaxy Note 9 (`SM-N960U1`) must be explicitly targeted with `-s 2aaaf879c51c7ece`.

> ⚠️ **IMPORTANT**: Never use `2aaaf879c51c7ece` for primary phone (S24 Ultra) or HealthOS tasks!

### Target Serial ID:
Always pass `-s 2aaaf879c51c7ece` ONLY when performing Note 9 tasks:
```bat
adb -s 2aaaf879c51c7ece <command>
```

## Keep Device Active During Debugging Mode (Prevent Screen-Off, Battery Save, and Wi-Fi Sleep)

To prevent the device from sleeping, locking, or dropping connection while in active debugging mode:

* **Enable Debugging Mode Settings:**
  ```bat
  # Set screen timeout to 30 mins (keeps screen on even on battery)
  adb -s 2aaaf879c51c7ece shell settings put system screen_off_timeout 1800000
  # Disable Battery Saver (prevents Wi-Fi/connection sleep)
  adb -s 2aaaf879c51c7ece shell settings put global low_power 0
  ```
* **Restore Default Settings (When Debugging is Done):**
  ```bat
  # Restore normal screen timeout (30 seconds)
  adb -s 2aaaf879c51c7ece shell settings put system screen_off_timeout 30000
  ```

Examples:
```bat
# Capture a screenshot
adb -s 2aaaf879c51c7ece shell screencap -p /sdcard/screenshot.png
adb -s 2aaaf879c51c7ece pull /sdcard/screenshot.png

# Check battery level
adb -s 2aaaf879c51c7ece shell dumpsys battery

# List installed packages
adb -s 2aaaf879c51c7ece shell pm list packages
```

---

## Safety Guidelines

* **Do NOT execute `phone.bat` commands:** The `phone` command-line toolkit located in the scratch directory is specifically written for the S24 Ultra ("Biggest") and its Termux/Tailscale environment. Running these commands will fail or target the wrong device.
* **Always verify connected status:** Check `adb devices` before starting work to confirm that the Note 9 is connected and authorized (`device` status, not `unauthorized`).
