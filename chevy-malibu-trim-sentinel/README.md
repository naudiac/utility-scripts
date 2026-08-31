# 🤖 Chevy Malibu Autonomous Trim Sentinel & Robot Mode Co-Pilot

A lightweight, deterministic, zero-token Python daemon and mobile web dashboard built for the **2013 Chevrolet Malibu ECO (2.4L LUK eAssist Mild Hybrid)**. 

Runs 100% locally on an Android phone (Termux) or in-car computer, linking to the car's **OBDLink MX+ Bluetooth bridge (`127.0.0.1:35000`)** to autonomously monitor fuel trims and clear lean codes without consuming a single AI token.

---

## ⚡ Key Features

1. **🤖 Autonomous Robot Mode (User-Controlled Arm/Disarm)**:
   - **Default State**: `DISARMED` (Completely idle until you explicitly arm it).
   - **Trigger Conditions**: Sustained High Long Term Fuel Trim ($LTFT \ge +22.0\%$) or Total Trim $\ge +28.0\%$ for $> 1.2$ seconds while engine is running ($RPM > 500$).
   - **Healing Action**: Automatically sends Mode 04 (`04\r`) to clear DTCs and reset learned fuel trim tables back to `0.0%`.
   - **Offline Android TTS**: Speaks a local alert via `termux-tts-speak` (*"Robot Mode: Fuel trim reached plus 24 percent. Resetting learned tables."*).
   - **Cooldown Guard**: Enforces a 75-second cooldown between wipes to avoid adaptation table thrashing.

2. **🚗 Live Automotive HUD & Diagnostics**:
   - 6 Real-time gauges: Engine RPM, Alternator Voltage, STFT, LTFT, MAF Airflow, Coolant Temp.
   - 60 FPS HTML5 Canvas waveform oscilloscope (STFT Cyan / LTFT Red).
   - 1-Tap Manual Actions: Read Live Trims, Mode 04 Adaptation Reset, Mode 03 DTC Scan.

3. **📁 Blackbox Flight Recorder & Git Sync**:
   - Records continuous 2.5 Hz CSV logs with timestamp, RPM, STFT, LTFT, MAF, MAP, Temp, and Volts.
   - Automatically saves freeze frame JSON snapshots of every auto-heal event.
   - 1-Tap sync pushes logs directly to this GitHub repository (`naudiac/utility-scripts`).

4. **🎙️ Universal Voice Co-Pilot & Distributed Swarm**:
   - Zero-credit Web Speech voice commands.
   - Direct bilateral RPC link across Tailscale WireGuard to Node Alpha (PC Master Station on port `8090`).

---

## 🚀 Installation & Usage

### 1. Run in Termux on Android (Samsung Galaxy S24 Ultra):
```bash
# Clone the repository
git clone https://github.com/naudiac/utility-scripts.git ~/utility-scripts

# Launch the daemon
python3 ~/utility-scripts/chevy-malibu-trim-sentinel/malibu_trim_sentinel.py
```

### 2. Access the Mobile Dashboard:
Open your mobile browser (Chrome / Samsung Internet) to:
👉 **`http://localhost:8080`**

### 3. Arming Robot Mode:
- Tap **`🛡️ ARM ROBOT AUTO-TRIM HEALER`** at the top of the dashboard when getting into the car for a drive.
- Tap **`🛑 DISARM ROBOT SENTINEL`** when you park or want manual control.

---

## 🔬 OBD-II PID Reference

| Parameter | PID | Description |
| :--- | :--- | :--- |
| **Engine RPM** | `010C` | Formula: `((A * 256) + B) / 4.0` |
| **Short Term Fuel Trim (STFT)** | `0106` | Formula: `(A - 128) * 100 / 128` |
| **Long Term Fuel Trim (LTFT)** | `0107` | Formula: `(A - 128) * 100 / 128` |
| **Mass Air Flow (MAF)** | `0110` | Formula: `((A * 256) + B) / 100.0` (g/s) |
| **Manifold Absolute Pressure (MAP)** | `010B` | Formula: `A` (kPa) |
| **Coolant Temp** | `0105` | Formula: `A - 40` (°C) |
| **Stored Fault Codes** | `03` | Mode 03 DTC Request |
| **Clear DTCs / Reset Adaptation** | `04` | Mode 04 Clear Diagnostic Information |
