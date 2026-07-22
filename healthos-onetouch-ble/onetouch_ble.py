"""
HealthOS - Direct Bluetooth LE sync module for OneTouch Verio Reflect meter.
Connects directly to the meter over Bluetooth, reads latest blood sugar readings,
and appends them to data/glucose_log.json.
"""
import asyncio
import json
import re
import datetime
from pathlib import Path

try:
    from bleak import BleakClient, BleakScanner
except ImportError:
    BleakClient = None

BASE_DIR = Path(__file__).parent.parent
JSON_PATH = BASE_DIR / "data" / "glucose_log.json"

RX_CHAR = "2dd10011-1c37-452d-8979-d1b4a787d0a4"
NT_CHAR = "2dd10013-1c37-452d-8979-d1b4a787d0a4"

TARGET_DEVICES = ["1JM-US-TBA3961A", "1JM-US-TBA4290A"]

def parse_glucose_values(raw_bytes: bytearray) -> list[int]:
    """Parse glucose readings from ASCII stream or LifeScan @-O nibble encoding."""
    readings = []
    
    # 1. Direct ASCII digits (e.g. '197', '170', '219')
    ascii_str = ''.join(chr(b & 0x7F) for b in raw_bytes)
    for match in re.findall(r'\b(\d{2,3})\b', ascii_str):
        val = int(match)
        if 40 <= val <= 500:
            readings.append(val)

    # 2. LifeScan hex-nibble encoding ('@'.. 'O' mapping 0..15)
    chars = [chr(b & 0x7F) for b in raw_bytes]
    nibbles = [ord(c) - ord('@') for c in chars if '@' <= c <= 'O']
    
    # 8-bit paired nibbles (e.g., 'J'+'J' = 0xAA = 170)
    for i in range(0, len(nibbles) - 1):
        val = (nibbles[i] << 4) | nibbles[i+1]
        if 40 <= val <= 500:
            readings.append(val)

    # 16-bit 4-nibble big-endian integers (e.g., '@'+'@'+'L'+'F' = 0x00C5 = 197)
    for i in range(0, len(nibbles) - 3):
        val16 = (nibbles[i] << 12) | (nibbles[i+1] << 8) | (nibbles[i+2] << 4) | nibbles[i+3]
        if 40 <= val16 <= 500:
            readings.append(val16)

    return readings

async def find_all_onetouch_meters():
    """Scan and return all advertising OneTouch meters."""
    if not BleakScanner:
        return []
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
    found = []
    for addr, (d, adv) in devices.items():
        name = d.name or adv.local_name or ""
        if any(target in name for target in TARGET_DEVICES) or "1JM-" in name or "OneTouch" in name:
            found.append((addr, name))
    found.sort(key=lambda item: next((i for i, t in enumerate(TARGET_DEVICES) if t in item[1]), 99))
    return found

async def sync_onetouch_ble(address: str = None) -> dict:
    """Connect to OneTouch meter over PC Bluetooth LE, parse reading, and append to glucose_log.json."""
    meters = []
    if address:
        meters = [(address, "OneTouch Meter")]
    else:
        meters = await find_all_onetouch_meters()

    if not meters:
        return {"ok": False, "error": "No OneTouch meter found advertising. Ensure Bluetooth is ON on your meter."}

    last_err = None
    for addr, meter_name in meters:
        received_bytes = bytearray()
        def callback(sender, data):
            received_bytes.extend(data)

        try:
            async with BleakClient(addr, timeout=8.0) as client:
                if not client.services.get_characteristic(NT_CHAR):
                    continue
                await client.start_notify(NT_CHAR, callback)
                
                for cmd_str in [b"RPR\r", b"RMR\r", b"DMP\r"]:
                    cmd_pkt = bytes([b | 0x80 for b in cmd_str])
                    await client.write_gatt_char(RX_CHAR, cmd_pkt, response=False)
                    await asyncio.sleep(2.5)

            readings = parse_glucose_values(received_bytes)
            if not readings:
                continue

            latest_value = readings[-1]

            # Load existing log
            existing_data = []
            if JSON_PATH.exists():
                with open(JSON_PATH, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)

            now_iso = datetime.datetime.now().isoformat()
            
            # Prevent exact duplicate entry within the last 2 minutes
            is_dup = False
            for entry in existing_data:
                if entry.get("value") == latest_value:
                    try:
                        entry_dt = datetime.datetime.fromisoformat(entry["timestamp"])
                        if (datetime.datetime.now() - entry_dt).total_seconds() < 120:
                            is_dup = True
                            break
                    except Exception:
                        pass

            if not is_dup:
                new_entry = {
                    "timestamp": now_iso,
                    "value": latest_value,
                    "type": "random",
                    "source": "onetouch_verio_reflect"
                }
                existing_data.append(new_entry)
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2)

            return {
                "ok": True,
                "address": addr,
                "meter": meter_name,
                "latest_reading": latest_value,
                "added_new": not is_dup,
                "timestamp": now_iso,
                "glucose_log_count": len(existing_data)
            }
        except Exception as e:
            last_err = str(e)
            continue

    return {"ok": False, "error": last_err or "Meters connected but no valid glucose value stream received."}

if __name__ == "__main__":
    res = asyncio.run(sync_onetouch_ble())
    print(json.dumps(res, indent=2))
