# 🚗 Car Sentinel: Standalone Android Package (`Sentinel.apk`) Product Architecture

**Date**: 2026-08-31  
**Author**: William Hanusiewicz (`naudiac`) & Antigravity  
**Repository**: `naudiac/utility-scripts`  
**Status**: DESIGN APPROVED • ANCHORED FOR IMPLEMENTATION  

---

## 📌 Executive Summary

This architecture specifies the first-principles transformation of the modular in-car vehicle telemetry and autonomous auto-trim healing prototype (previously running via Termux, Python, and `BT/TCP Bridge Pro`) into a single, standalone, commercial-grade Android Application Package (**`Sentinel.apk`**).

The design explicitly caters to **older and modern Android smartphones** (Android 7.0 Nougat / API 24 through Android 15 / API 35) with zero dependencies on third-party bridge apps, terminal environments, or manual command-line setups.

---

## 🏗️ First-Principles System Architecture

```mermaid
flowchart TD
    subgraph Vehicle ["🚗 Vehicle Diagnostic Interface"]
        ECU["Vehicle Engine Control Module (ECM)"]
        OBD["Bluetooth OBD-II Adapter\n(OBDLink MX+, vLinker, ELM327)"]
        ECU <-->|CAN ISO 15765 / SAE J1979| OBD
    end

    subgraph APK ["📦 Sentinel.apk (Single Standalone Android App)"]
        subgraph Layer1 ["1. Direct Hardware Transport"]
            BT_RFCOMM["Android BluetoothSocket (RFCOMM / SPP)\nUUID: 00001101-0000-1000-8000-00805F9B34FB\n• Auto-discovery of paired adapters\n• Zero third-party bridge apps\n• Zero local socket port collisions"]
        end

        subgraph Layer2 ["2. Unkillable Foreground Service (Core Engine)"]
            Service["Android ForegroundService\n(foregroundServiceType=connectedDevice)\n• Kernel-level CPU keep-alive (Zero Sleep)\n• Sticky Status Bar Notification HUD"]
            
            CAN_Poller["5 Hz High-Speed Telemetry Poller\n(RPM, STFT, LTFT, MAF, MAP, Temp, Volts)"]
            
            Watchdog["Autonomous Auto-Trim Healer\n• Deceleration vacuum spike filter\n• Moving average fuel trim analyzer\n• Autonomous Mode 04 clear dispatcher"]
            
            Service --> CAN_Poller
            Service --> Watchdog
        end

        subgraph Layer3 ["3. Native Android Audio Pipeline"]
            TTS["Android TextToSpeech (STREAM_MUSIC)\n• Direct OS hardware routing\n• Transient audio focus & music ducking\n• Zero web browser gesture restrictions"]
        end

        subgraph Layer4 ["4. Embedded Native HUD & Flight Recorder"]
            HUD["Clean Automotive Dark-Mode HUD\n• Real-time Cyan/Red Fuel Trim Waveforms\n• 1-Tap [🛡️ ARM ROBOT] Toggle\n• Offline CSV Flight Recorder"]
        end

        BT_RFCOMM <--> CAN_Poller
        Watchdog -->|Trigger Diagnostics & Alerts| TTS
        CAN_Poller -->|Live Telemetry Feed| HUD
    end

    OBD <-->|Bluetooth SPP| BT_RFCOMM
```

---

## 📱 Hardware & OS Compatibility Matrix

| Parameter | Specification | Purpose |
| :--- | :--- | :--- |
| **Minimum SDK** | `minSdk = 24` (Android 7.0 Nougat) | Full backward compatibility for phones back to 2016 (including older Galaxy devices). |
| **Target SDK** | `targetSdk = 34` (Android 14) | Compliance with modern Android security and foreground service type standards. |
| **Legacy Bluetooth** | `BLUETOOTH`, `BLUETOOTH_ADMIN`, `ACCESS_FINE_LOCATION` | Seamless execution on Android 11 and older (API $\le$ 30). |
| **Modern Bluetooth** | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` | Runtime permission requests on Android 12+ (API $\ge$ 31). |
| **Memory Footprint** | `< 25 MB RAM` | Smooth operation on low-spec 2GB/3GB RAM devices. |
| **Binary Footprint** | `< 4 MB APK` | Ultra-fast download and zero bloat. |

---

## 🔄 The Turnkey 1-Tap Experience for Dad

1. **One-Time Installation**:
   * William sends `Sentinel.apk` to Dad via WhatsApp or Google Drive.
   * Dad taps the file and presses **Install**.
   * Opens the app, selects his OBD adapter from paired devices, and taps **START GUARDIAN**.
2. **Everyday Commute (Zero Friction)**:
   * Dad starts his car.
   * Phone detects OBD Bluetooth link and announces:
     > *"Vehicle linked. Live telemetry active. Guardian armed."*
   * Dad locks his phone or runs Google Maps. The foreground service monitors fuel trims 24/7.
   * If a lean spike occurs ($\ge +22\%$), the robot automatically dispatches Mode 04 and announces:
     > *"Lean fuel trim spike cleared. Adaptations restored."*

---

## 🚀 Implementation Roadmap (When Resuming)

1. **Scaffold Project Structure**: Generate clean Gradle / Kotlin project with `empty-activity` template via `android create`.
2. **Implement RFCOMM & Foreground Service**: Port OBDLink communication loop and PID parser from `malibu_trim_sentinel.py`.
3. **Integrate Native Text-to-Speech & Canvas HUD**: Wire Android TTS audio ducking and real-time waveform view.
4. **Compile & Road Test**: Compile `Sentinel.apk` on PC, deploy to William's S24 Ultra for live road validation, and distribute to Dad.
