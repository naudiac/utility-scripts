---
name: phone-control-s24
description: >
  Control William's Android phone ("Biggest", Samsung Galaxy S24 Ultra) remotely
  from the PC via ADB over Wi-Fi or SSH. Use when the user asks to send a text, check
  battery, mirror the screen, launch an app, take a screenshot, manage files,
  read messages, toggle Wi-Fi/data/Bluetooth, sync wallpapers, or perform any action on the S24 phone.
---

# Samsung Galaxy S24 Ultra ("Biggest") Control Skill

## Overview

William has a fully built CLI toolkit to remotely control his primary Android phone over Wi-Fi using ADB and SSH.

* **Phone:** Biggest — Samsung Galaxy S24 Ultra (SM-S928U1)
* **Android:** 16 (SDK 36)
* **Screen Resolution:** 1440 × 3120 pixels

---

## ADB Device Identification Matrix (CRITICAL)

| Device Name | Model | Connection | ADB Target Serial | Primary Role |
| :--- | :--- | :--- | :--- | :--- |
| **S24 Ultra ("Biggest")** | `SM-S928U1` | Wi-Fi Wireless Debugging | `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` | **Primary phone: HealthOS, BP, Diet, SMS, Apps** |
| **Galaxy Note 9** | `SM-N960U1` | USB Cable | `2aaaf879c51c7ece` | Secondary test phone — **DO NOT USE FOR S24 TASKS** |
| **Galaxy Watch5 Pro** | `SM-R920` | Wi-Fi Wireless Debugging | `adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp` | Smartwatch ONLY |

---

## Wireless Debugging & Persistent mDNS Target Selection

When connecting to the Samsung Galaxy S24 Ultra ("Biggest", model `SM-S928U1`) over Wi-Fi:

1. **Do NOT rely solely on static IP:port numbers** (e.g. `192.168.4.83:43707`), as Android re-keys Wireless Debugging ports dynamically upon Wi-Fi reconnection or reboot.
2. **Use the Persistent mDNS Service Target String**:
   ```bat
   adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp <command>
   ```
   * Modern Android (11+) advertises over local mDNS (`_adb-tls-connect._tcp`).
   * ADB automatically resolves `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` to the phone's active dynamic IP and port!
3. **Multi-Device Disambiguation:** When multiple devices are connected (`2aaaf879c51c7ece` = Note 9, `adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp` = S24 Ultra), **ALWAYS** pass `-s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp`. NEVER pass `2aaaf879c51c7ece` when working on the S24 Ultra!

## Keep Device Active During Debugging Mode (Prevent Screen-Off, Battery Save, and Wi-Fi Sleep)

To prevent the device from sleeping, locking, or dropping connection while in active debugging mode:

* **Enable Debugging Mode Settings:**
  ```bat
  # Set screen timeout to 30 mins (keeps screen on even on battery)
  adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell settings put system screen_off_timeout 1800000
  # Disable Battery Saver (prevents Wi-Fi/connection sleep)
  adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell settings put global low_power 0
  ```
* **Restore Default Settings (When Debugging is Done):**
  ```bat
  # Restore normal screen timeout (2 mins)
  adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp shell settings put system screen_off_timeout 120000
  ```

---

## SSH Terminal Connection (Primary Control Method)

A direct SSH tunnel into Termux gives full terminal access without any UI hacks.

* **CRITICAL FALLBACK RULE:** If `phone.py` fails to connect via SSH (e.g., `ERROR: Could not establish SSH connection to phone`), DO NOT give up. Immediately fall back to using the ADB-based batch scripts (e.g., `cmd /C "phone.bat screenshot"`) as they are often more reliable when Termux/Tailscale is asleep.

### SSH Details:
* **LAN Host:** `192.168.4.83` (fast — used when phone is on same WiFi)
* **Tailscale Host:** `100.120.126.34` (fallback — works over 4G or any network)
* **Port:** `8022` (Termux sshd)
* **Key:** `C:\Users\whanusiewicz\.gemini\antigravity\scratch\phone-cli\termux_rsa`
* **Python wrapper:** `C:\Users\whanusiewicz\.gemini\antigravity\scratch\phone-cli\phone.py`
* **Config:** `C:\Users\whanusiewicz\.gemini\antigravity\scratch\phone-cli\phone_config.json`

### phone.py usage:
```
python phone.py --battery              # Battery status via termux-battery-status
python phone.py --sms "+1..." "msg"    # Send SMS via termux-sms-send
python phone.py --screenshot path.png  # Screenshot via termux-screenshot
python phone.py --wallpaper img.jpg    # Set wallpaper (home + lock)
python phone.py --wallpaper-pc         # Match phone wallpaper to PC desktop
python phone.py --wallpaper-color black  # Solid color wallpaper
python phone.py "any shell command"    # Run anything in Termux environment
python phone.py --check                # Verify connection + show route used
```

---

## Strict Rule: Quiet Backend Extraction (No GUI Touch Input)

* **Do NOT use GUI automation for health/vitals data harvesting**: Never use `input tap`, `input swipe`, `monkey` app launcher, or `uiautomator dump` UI screen navigation to pull health, step, or vitals data. Screen pops and visible app switching disrupt the user.
* **Use Quiet Background APIs & Services**:
  * **Step counters & calories**: Parse live `logcat -d` streams (`SHEALTH#PedometerService: onCombinedDataChanged`) or `dumpsys sensorservice`.
  * **Skin temperature & thermals**: Query `dumpsys thermalservice`.
  * **Blood pressure & Glucose**: Parse SDK debug logs (`ihealth_sdk/*.txt`), BLE packet payloads (`0x4A` packets), or background SQLite files.

---

## Bypassing FLAG_SECURE (Screenshot-Blocked Apps)

Many apps (banking, pharmacy, health, insurance) block ADB screenshots using `FLAG_SECURE`. When `screenshot` returns a **solid black image (~5KB)**, the app has this protection enabled.

### Detection
A screenshot is FLAG_SECURE-blocked if:
* Image file is ~5KB (real content would be 200KB–2MB)
* Image renders completely black

### Bypass: Use `get_ui_tree` Instead
The Android Accessibility API bypasses FLAG_SECURE entirely. Use `get_ui_tree` to read all visible text, labels, and button descriptions directly from the app's view hierarchy.

**Navigation pattern for FLAG_SECURE apps:**
1. `launch_app(package_name)` — launch the app
2. `tap(x, y)` / `swipe()` — navigate (coordinates still work even blind)
3. `get_ui_tree()` — read all text from the current screen
4. Repeat steps 2–3 to traverse the full app

**Known FLAG_SECURE apps on William's phone:**
* CVS Pharmacy (`com.cvs.launchers.cvs`) — Prescription section
* Banking apps — account/transaction screens
* Password managers — vault screens
* MyChart / Epic — health record screens

---

## Toolkit Location

```
C:\Users\whanusiewicz\.gemini\antigravity\scratch\
  phone.bat       ← main launcher (run this from any terminal)
  phone.ps1       ← full logic engine (40+ commands)
  adb.bat         ← ADB wrapper pre-configured for Biggest
  sq.bat          ← SQLite wrapper for Phone Link message DB
```

Run commands:
```bat
cd C:\Users\whanusiewicz\.gemini\antigravity\scratch
phone <command> [args]
```

---

## Full Command Reference

### Screen & Control
```
phone mirror              Stream screen to PC (scrcpy — full mouse/keyboard control)
phone mirror off          Mirror with phone screen off
phone screenshot          Capture screen, auto-open on PC
phone record [file.mp4]   Record screen to MP4
phone tap X Y             Tap a screen coordinate
phone swipe X1 Y1 X2 Y2  Swipe gesture
phone type TEXT           Type text on screen
phone key NAME            Send key: home back recents power volup voldown enter
phone home                Go to home screen
phone back                Press back
phone lock                Lock screen
phone unlock              Wake + swipe-to-unlock
phone uidump              Dump UI element tree (find tap coordinates)
```

### Messaging (reads via Phone Link DB, sends via ADB intent)
```
phone inbox               Show recent conversations with thread IDs
phone read THREAD_ID      Read a full conversation
phone send NUMBER MESSAGE  Send SMS/RCS
phone search KEYWORD      Search message history
```

**Phone Link message DB path:**
`C:\Users\whanusiewicz\AppData\Local\Packages\Microsoft.YourPhone_8wekyb3d8bbwe\LocalCache\Indexed\0f4f538e-7dad-4b7f-bd95-322b593f1824\System\Database\phone.db`  
Table: `message` — columns: `thread_id`, `from_address`, `to_address`, `body`, `timestamp`

### Notifications
```
phone notifs              Show current notifications (dumpsys)
phone notifs watch        Live notification monitor (Ctrl+C to stop)
```

### System Toggles
```
phone wifi on/off         Toggle Wi-Fi (svc wifi enable/disable) [ADB only]
phone data on/off         Toggle mobile data
phone bluetooth on/off    Toggle Bluetooth
phone airplane on/off     Airplane mode
phone doze on/off         Battery doze mode
phone volume up/down/mute Volume control
phone brightness N        Set brightness 0–255
phone rotate auto/landscape/portrait
```

### Apps
```
phone open APP            Launch by friendly name or package
phone apps                List installed user apps
phone kill APP            Force-stop app
phone clear APP           Clear app data/cache
phone install PATH.APK    Install APK
phone uninstall PACKAGE   Remove app
phone debloat PACKAGE     Disable bloatware (no root needed)
phone restore PACKAGE     Re-enable a disabled app
```

**Friendly app name → package map (built-in):**
```
messages   → com.google.android.apps.messaging
chrome     → com.android.chrome
youtube    → com.google.android.youtube
spotify    → com.spotify.music
maps       → com.google.android.apps.maps
camera     → com.sec.android.app.camera
settings   → com.android.settings
whatsapp   → com.whatsapp
instagram  → com.instagram.android
gmail      → com.google.android.gm
photos     → com.google.android.apps.photos
robinhood  → com.robinhood.android
facebook   → com.facebook.katana
netflix    → com.netflix.mediaclient
reddit     → com.reddit.frontpage
tiktok     → com.zhiliaoapp.musically
```

### Device Info
```
phone battery             Level, status, temp, voltage
phone info                Model, Android version, serial, CPU
phone wifi-info           Wi-Fi SSID, signal, IP
phone storage             Storage usage (df -h)
phone procs               Top running processes
phone settings global/secure/system   Dump system settings
```

### Files
```
phone ls [PATH]           List files (default: /sdcard)
phone pull REMOTE [LOCAL] Copy from phone to PC (default local: scratch dir)
phone push LOCAL REMOTE   Copy from PC to phone
phone find NAME           Search files by name on /sdcard
phone screenshots         List recent screenshots on phone
phone photos              List recent DCIM/Camera photos
```

### Calls
```
phone call NUMBER         Dial a number
phone hangup              End current call
```

### Fix Phone Link Clipboard Sync
When cross-device copy/paste stops working, restart the sync stack:
1. **On Phone:** Run `phone shell am force-stop com.microsoft.appmanager`
2. **On PC:** Run `Stop-Process -Name PhoneExperienceHost -Force` and `Start-Process ms-phone:` in PowerShell.

---

## Wallpaper Control

Set wallpaper via SSH → `termux-wallpaper`. Always set BOTH home (-f) and lock (-l).

### Match PC wallpaper to phone:
Run `python phone.py --wallpaper-pc`

### Set a solid color wallpaper:
Run `python phone.py --wallpaper-color black`

---

## Google Drive Backup

The phone CLI files are backed up to Google Drive:  
**Gemini Experiments → phone-cli/** (ID: `1Yit5cc1I9VP8jERFzGFgX5-CiLMUJKNs`)

To re-upload after changes:
```bat
cd C:\Users\whanusiewicz\.gemini\antigravity\scratch\Google_Drive_Tools_Kit
python upload_phone_cli.py
```
