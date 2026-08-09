---
name: watch-control-g5pro
description: >
  Control William's Samsung Galaxy Watch5 Pro Wear OS smartwatch remotely
  from the PC via ADB over Wi-Fi. Use when the user asks to check watch status,
  modify watch scales/animations, manage Wear OS packages, or pull health/vitals data.
---

# Samsung Galaxy Watch5 Pro ("NBTR") Control Skill

## Overview

This skill is for controlling and debugging William's smartwatch.

* **Watch:** Galaxy Watch5 Pro (SM-R920)
* **OS:** Wear OS 6 / One UI Watch 6.5 (Android 16, SDK 36)
* **Connection Type:** Wi-Fi Wireless Debugging / Bluetooth Port Forwarding

---

## Wireless Debugging & Persistent mDNS Target Selection

When connecting to the Galaxy Watch5 Pro (`SM-R920`) over Wi-Fi:

1. **Do NOT rely solely on static IP:port numbers** (e.g. `192.168.4.122:45867`), as Wear OS re-keys Wireless Debugging ports dynamically upon Wi-Fi reconnection or reboot.
2. **Use the Persistent mDNS Service Target String**:
   ```bat
   adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp <command>
   ```
   * Wear OS (4+) advertises over local mDNS (`_adb-tls-connect._tcp`).
   * ADB automatically resolves `adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp` to the watch's active dynamic IP and port!
3. **Multi-Device Disambiguation:** Always pass `-s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp` to all ADB commands to avoid executing commands on the S24 Ultra or Note 9.

## Keep Device Active During Debugging Mode (Prevent Screen-Off, Battery Save, and Wi-Fi Sleep)

To prevent the watch face from sleeping, locking, or dropping Wi-Fi connection while in active debugging mode:

* **Enable Debugging Mode Settings:**
  ```bat
  # Set screen timeout to 30 mins (keeps screen on even on battery)
  adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell settings put system screen_off_timeout 1800000
  # Disable Battery Saver (prevents Wi-Fi/connection sleep)
  adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell settings put global low_power 0
  ```
* **Restore Default Settings (When Debugging is Done):**
  ```bat
  # Restore normal screen timeout (30 seconds)
  adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell settings put system screen_off_timeout 30000
  ```

---

## Bluetooth Debugging Bridge (Fallback Method)

If the watch Wi-Fi is disabled, you can tunnel ADB through the S24 Ultra's Bluetooth connection:

1. Enable **Bluetooth Debugging** in Developer Options on the Watch.
2. In the **Galaxy Wearable** app on the S24 Ultra -> Watch Settings -> About watch -> Tap the software version 7 times to unlock wearable developer settings, and enable **Debugging over Bluetooth**.
3. Establish a port forward from the PC to the phone's bluetooth debug socket:
   ```bat
   adb -s adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp forward tcp:4444 localabstract:adb:bluetooth
   ```
4. Connect to the forwarded port:
   ```bat
   adb connect localhost:4444
   ```
5. Target the watch using:
   ```bat
   adb -s localhost:4444 <command>
   ```

---

## Strict Rule: Quiet Backend Health/Vitals Data Extraction

* **Do NOT use GUI automation or touch simulation**: Never use `input tap`, `input swipe`, or screenshot parsing to extract heart rate, step count, or other health data. Visible app switching disrupts the user's wrist experience.
* **Quiet logcat and database harvesting:**
  * **Steps & Activity:** Parse live `logcat -d` streams filtering for pedometer services:
    ```bat
    adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell "logcat -d | grep -i pedometer"
    ```
  * **Vitals & Sensors:** Read battery/thermal states via:
    ```bat
    adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell dumpsys thermalservice
    adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell dumpsys battery
    ```

---

## UI Speedup & Snappiness settings

Reduce UI animation scales to `0.0` for instantaneous responses on the watch screen:
```bat
adb -s adb-RFAW51DNBTR-52u2PZ._adb-tls-connect._tcp shell "settings put global window_animation_scale 0.0; settings put global transition_animation_scale 0.0; settings put global animator_duration_scale 0.0"
```

---

## Disabled System Bloatware

To preserve RAM and battery life, these background services have been disabled-user on the watch:
* `com.google.android.wearable.assistant` (Google Assistant background listening)
* `com.samsung.android.bixby.wakeup` (Bixby voice wakeup background listening)
* `com.samsung.android.samsungpay.gear` (Samsung Pay)
* `com.google.android.apps.walletnfcrel` (Google Wallet)
* `com.google.android.apps.wearable.retailattractloop` (Retail Demo loop)
* `com.samsung.android.dqagent` (Diagnostic logging agent)
* `com.samsung.android.wearable.setupwizard.fota` (Setup wizard leftovers)
