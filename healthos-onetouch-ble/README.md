# HealthOS — OneTouch Verio Reflect BLE Direct Sync

Direct Python Bluetooth LE (Bleak) sync utility for LifeScan / OneTouch Verio Reflect blood glucose meters. 
Connects over PC Bluetooth, sends MSB-framed command packets, decodes notifications (ASCII digit streams & LifeScan `@`–`O` hex-nibble byte arrays), and logs readings directly to `HealthOS/data/glucose_log.json`.

## Features
- **Zero-phone dependency**: Communicates directly over PC Bluetooth LE.
- **Dual Stream Parsing**: Handles both raw ASCII numeric records and LifeScan byte-nibble encodings.
- **De-duplication**: Prevents duplicate log entries within a 2-minute window.
- **GATT Integration**: Targets service `2dd10010-1c37-452d-8979-d1b4a787d0a4`.

## Usage
```powershell
python onetouch_ble.py
```
