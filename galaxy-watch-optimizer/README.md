# Galaxy Watch (Wear OS) Optimizer

Automated PowerShell script and guide for optimizing Samsung Galaxy Watches (Galaxy Watch 4, 5, 6, 7, Ultra) running Wear OS / One UI Watch over Wi-Fi ADB.

---

## ⚡ Key Optimizations Included

1. **Instant UI Responsiveness (`0.0x` Animation Scales)**
   - Sets `window_animation_scale`, `transition_animation_scale`, and `animator_duration_scale` to `0.0`.
   - Eliminates micro-stutter and animation delays across apps, tiles, and notification popups.

2. **Background Voice Wakeup Disabling (Battery & RAM Saver)**
   - Disables background microphone listening for `com.samsung.android.bixby.wakeup` ("Hi Bixby") and `com.google.android.wearable.assistant` ("Hey Google").
   - Saves **~70MB+ background RAM** and reduces passive battery drain.

3. **Contactless Payment App Disabling**
   - Disables unused watch payment frameworks (`Samsung Pay` & `Google Wallet`).

4. **Diagnostic & Store Bloatware Removal**
   - Disables `com.samsung.android.dqagent` (Samsung diagnostic tracking agent — saves **~38MB RAM**).
   - Disables `com.google.android.apps.wearable.retailattractloop` (store demo loop).
   - Disables setup wizard FOTA leftovers (`com.samsung.android.wearable.setupwizard.fota`).

---

## 🚀 Quick Start Guide

### 1. Enable Wireless Debugging on Watch
1. On Galaxy Watch, go to **Settings** > **About watch** > **Software info**.
2. Tap **Software version** 7 times to enable **Developer options**.
3. Go back to **Settings** > **Developer options**.
4. Enable **ADB debugging** and **Wireless debugging**.
5. Tap **Wireless debugging** > **Pair new device**.

### 2. Pair and Connect from PC
```powershell
# Pair PC with watch (using port & 6-digit code shown under 'Pair new device')
adb pair <WATCH_IP>:<PAIR_PORT> <6_DIGIT_CODE>

# Connect via Wireless Debugging port
adb connect <WATCH_IP>:<CONNECT_PORT>
```

### 3. Run Optimization Script
```powershell
.\Optimize-GalaxyWatch.ps1
```

---

## 🔄 Reversion Commands
To re-enable any disabled package or restore default animation speeds:

```powershell
# Reset animation scales back to 1.0x default
adb shell settings put global window_animation_scale 1.0
adb shell settings put global transition_animation_scale 1.0
adb shell settings put global animator_duration_scale 1.0

# Re-enable a disabled package (example: Google Assistant)
adb shell pm enable com.google.android.wearable.assistant
```
