---
name: firetv-dev-setup
description: >
  Full roadmap and execution guide for gaining developer access to the living room
  Fire TV stick(s), installing BusyBox + Termux, setting up SSH, loading AGY CLI,
  and integrating with the Samsung TV into a unified AGY-controlled living room system.
  Trigger when the user asks to work on the Fire Stick, sideload apps, develop on the
  Fire TV, or control the living room as a unified system.
---

# Fire TV Developer Setup — Living Room System

## Goal
AGY controls the living room as a single unified system:
- **Samsung TU7000 TV** → SmartThings cloud API (✅ complete)
- **Fire TV Stick** → ADB over Wi-Fi + Termux SSH
- Unified skill: "switch to Netflix", "pause", "turn off the room", etc.

---

## Current State (as of 2026-07-08)

| Device | IP | MAC | ADB | Status |
|---|---|---|---|---|
| Fire TV Stick A | `192.168.4.36` | `90:23:5b:e1:9d:cf` | Port 5555 closed | Developer mode OFF |
| Fire TV Stick B | `192.168.4.39` | `7c:63:05:4d:56:a9` | Port 5555 OPEN | Developer mode ON ✅ |
| Samsung TV (WiFi) | `192.168.4.44` | `70:09:71:27:4c:bc` | N/A | SmartThings ✅ |

**Unknown**: Which Fire Stick is physically on HDMI1 of the living room TV.
The TV's HDMI1 input is labeled "Amazon Fire TV stick" in SmartThings.
Father is using the TV — identify when it's free.

---

## Phase 1 — Identify & Authorize ADB

### Step 1a: Identify which stick is on HDMI1
```powershell
# Switch TV to HDMI1 via SmartThings and observe
$h = @{ Authorization = "Bearer <YOUR_SMARTTHINGS_PAT>"; "Content-Type" = "application/json" }
Invoke-RestMethod "https://api.smartthings.com/v1/devices/cc6c7a3a-74cc-16eb-14eb-83267b2b27a2/commands" `
  -Method Post -Headers $h `
  -Body '{"commands":[{"component":"main","capability":"samsungvd.mediaInputSource","command":"setInputSource","arguments":["HDMI1"]}]}'
```
Then look at what Fire TV home screen appears. Alternatively, attempt ADB connect to `.39`:
- If authorization dialog appears ON the living room TV → `.39` is on HDMI1
- If no dialog → `.39` is the other TV, `.36` is on HDMI1

### Step 1b: Authorize ADB on .39 (already open)
```powershell
$adb = "C:\Users\whanusiewicz\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"

# Attempt connection — watch Fire TV screen for "Allow USB debugging?" dialog
& $adb connect 192.168.4.39:5555
# On Fire TV screen: check "Always allow from this computer" → Allow
& $adb -s 192.168.4.39:5555 shell "getprop ro.product.model"
```

### Step 1c: Enable Developer Mode on .36 (if needed)
On the Fire TV remote:
1. **Settings → My Fire TV → About**
2. Click **"Fire TV Stick"** (build info) **7 times** → "You are now a developer"
3. **Settings → My Fire TV → Developer Options → ADB Debugging → ON**
4. **Settings → My Fire TV → Developer Options → Apps from Unknown Sources → ON**

Then connect:
```powershell
& $adb connect 192.168.4.36:5555
```

---

## Phase 2 — BusyBox (Lightweight Linux Tools)

```powershell
# Download BusyBox ARM binary
Invoke-WebRequest "https://busybox.net/downloads/binaries/1.35.0-arm-linux-musleabi/busybox" -OutFile "$env:TEMP\busybox"

# Push to Fire TV
& $adb -s 192.168.4.39:5555 push "$env:TEMP\busybox" /data/local/tmp/busybox
& $adb -s 192.168.4.39:5555 shell "chmod 755 /data/local/tmp/busybox"
& $adb -s 192.168.4.39:5555 shell "/data/local/tmp/busybox --help"

# Install all applets
& $adb -s 192.168.4.39:5555 shell "/data/local/tmp/busybox --install /data/local/tmp/"
```

Provides: `bash`, `wget`, `grep`, `awk`, `sed`, `curl`, `tar`, `find`, and 200+ Linux tools.

---

## Phase 3 — Termux via Sideload

```powershell
# Download Termux APK (F-Droid build, ARM64 — NOT Google Play version)
Invoke-WebRequest "https://f-droid.org/repo/com.termux_118.apk" -OutFile "$env:TEMP\termux.apk"

# Sideload (requires "Apps from Unknown Sources" enabled)
& $adb -s 192.168.4.39:5555 install "$env:TEMP\termux.apk"

# Launch Termux on Fire TV screen
& $adb -s 192.168.4.39:5555 shell "am start -n com.termux/.HomeActivity"
```

### Termux Setup (run inside Termux on Fire TV)
```bash
pkg update -y
pkg install -y openssh python3

# Copy SSH key from phone setup
mkdir -p ~/.ssh
# Push PC's public key
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys

# Start SSH daemon
sshd
```

Then from PC:
```powershell
ssh -i "C:\Users\whanusiewicz\.gemini\antigravity\scratch\phone-cli\termux_rsa" -p 8022 192.168.4.39
```

---

## Phase 4 — AGY CLI on Fire TV

```bash
# Inside Fire TV Termux via SSH:
pkg install -y curl

# Install AGY CLI (same as phone)
curl -fsSL https://storage.googleapis.com/cloud-code-daily/agy/install.sh | bash

# Or copy binary directly from phone via SCP
scp -P 8022 192.168.4.83:/path/to/agy 192.168.4.39:/data/data/com.termux/files/usr/bin/agy
```

---

## Phase 5 — Unified Room Control Skill

Once all above is complete, the unified living room commands will be:

| Command | Action | Method |
|---|---|---|
| "Turn on the room" | TV on | SmartThings switch.on |
| "Switch to Fire TV" | HDMI1 input | SmartThings setInputSource |
| "Switch to live TV" | dtv input | SmartThings setInputSource |
| "Pause" | Fire TV pause | ADB input keyevent 85 |
| "Play" | Fire TV play | ADB input keyevent 85 |
| "Volume up/down N" | TV volume | SmartThings setVolume |
| "Mute" | TV mute | SmartThings mute |
| "Turn off the room" | TV off | SmartThings switch.off |
| "Open Netflix" | Launch app | ADB am start intent |
| "Go home" | Fire TV home | ADB input keyevent 3 |

### ADB Key Events Reference
```powershell
$adb = "...\adb.exe"
$tv  = "192.168.4.39:5555"

& $adb -s $tv shell "input keyevent 85"   # Play/Pause
& $adb -s $tv shell "input keyevent 4"    # Back
& $adb -s $tv shell "input keyevent 3"    # Home
& $adb -s $tv shell "input keyevent 164"  # Mute
& $adb -s $tv shell "input keyevent 24"   # Volume Up
& $adb -s $tv shell "input keyevent 25"   # Volume Down
& $adb -s $tv shell "input keyevent 19"   # D-pad Up
& $adb -s $tv shell "input keyevent 20"   # D-pad Down
& $adb -s $tv shell "input keyevent 21"   # D-pad Left
& $adb -s $tv shell "input keyevent 22"   # D-pad Right
& $adb -s $tv shell "input keyevent 23"   # D-pad Select/OK
```

---

## SmartThings Reference (already complete)
See: `samsung-tv-smartthings` skill for full TV control commands.
Token: `<YOUR_SMARTTHINGS_PAT>`
Device ID: `cc6c7a3a-74cc-16eb-14eb-83267b2b27a2`
