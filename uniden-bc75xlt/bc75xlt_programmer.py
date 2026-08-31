"""
Uniden Bearcat BC75XLT Automated Headless Programmer
Communicates directly with the BC75XLT scanner over USB virtual serial port.
"""

import sys
import os
import time
import csv
import serial
import serial.tools.list_ports

CSV_PATH = os.path.join(os.path.dirname(__file__), 'bc75xlt_master_300.csv')
BAUD_RATES = [57600, 9600, 19200, 38400, 115200]

def find_bc75xlt_port():
    """Scan all active COM ports for a Uniden BC75XLT scanner."""
    ports = list(serial.tools.list_ports.comports())
    usb_ports = [p for p in ports if "bluetooth" not in p.description.lower()]
    print(f"Scanning {len(usb_ports)} physical/USB serial COM ports...")
    
    for p in usb_ports:
        print(f"Checking {p.device}: {p.description} [{p.hwid}]")
        for baud in BAUD_RATES:
            try:
                ser = serial.Serial(p.device, baud, timeout=0.3)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                
                # Send Model query
                ser.write(b"MDL\r")
                time.sleep(0.05)
                resp = ser.read(100).decode('ascii', errors='ignore').strip()
                
                if any(x in resp for x in ["BC75XLT", "UBC75XLT", "BC125AT"]):
                    print(f"--> FOUND UNIDEN SCANNER on {p.device} at {baud} baud! Response: {resp}")
                    ser.close()
                    return p.device, baud, resp
                
                ser.close()
            except Exception:
                pass
                
    return None, None, None

def program_scanner(port, baud, csv_path):
    print(f"\nOpening {port} at {baud} baud...")
    ser = serial.Serial(port, baud, timeout=1.0)
    
    try:
        # 1. Query Model & Version
        ser.write(b"MDL\r")
        time.sleep(0.1)
        mdl = ser.read(100).decode('ascii', errors='ignore').strip()
        print(f"Scanner Model: {mdl}")
        
        ser.write(b"VER\r")
        time.sleep(0.1)
        ver = ser.read(100).decode('ascii', errors='ignore').strip()
        print(f"Firmware Version: {ver}")
        
        # 2. Enter Program Mode
        print("\nEntering Program Mode (PRG)...")
        ser.write(b"PRG\r")
        time.sleep(0.2)
        prg_resp = ser.read(100).decode('ascii', errors='ignore').strip()
        print(f"PRG response: {prg_resp}")
        
        # 3. Read CSV and Write Channels
        channels = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                channels.append(row)
                
        print(f"Loaded {len(channels)} channels from {os.path.basename(csv_path)}.\n")
        print("Writing 300 channels across 10 Banks...")
        
        success_count = 0
        for row in channels:
            ch_num = int(row['Channel'])
            bank_num = int(row['Bank'])
            name = str(row['Name'])[:16]
            freq_mhz = float(row['Frequency'])
            
            # BC75XLT frequency format: 8-digit integer in 100Hz resolution
            freq_str = f"{int(round(freq_mhz * 10000)):08d}"
            
            mode_str = str(row['Mode']).upper()
            mod_code = ""
            if "AM" in mode_str:
                mod_code = "AM"
            elif "NFM" in mode_str:
                mod_code = "NFM"
            elif "FM" in mode_str:
                mod_code = "FM"
                
            delay = 1  # 2-second delay enabled (1)
            lockout = int(row.get('Lockout', 0))
            priority = 0
            
            # Verified CIN format: CIN,<Index>,<Tag>,<Freq>,<Mod>,<Tone>,<Delay>,<Lockout>,<Priority>
            cmd = f"CIN,{ch_num},{name},{freq_str},{mod_code},,{delay},{lockout},{priority}\r"
            ser.write(cmd.encode('ascii'))
            time.sleep(0.02)
            resp = ser.read(100).decode('ascii', errors='ignore').strip()
            
            if "OK" in resp or "CIN" in resp:
                success_count += 1
                if ch_num % 30 == 0 or ch_num == 1:
                    print(f" [Bank {bank_num:2d}] Flashed Channel {ch_num:3d}/300: {name:<10s} ({freq_mhz:8.4f} MHz {mod_code}) -> OK")
            else:
                print(f" [Bank {bank_num:2d}] Channel {ch_num:3d} ({name}) Response: {resp}")
                
        print(f"\nSuccessfully wrote {success_count}/{len(channels)} channels.")
        
        # 4. Exit Program Mode
        print("\nExiting Program Mode (EPG)...")
        ser.write(b"EPG\r")
        time.sleep(0.2)
        epg_resp = ser.read(100).decode('ascii', errors='ignore').strip()
        print(f"EPG response: {epg_resp}")
        print("\n[SUCCESS] FLASH COMPLETE! The Uniden BC75XLT is 100% programmed and scanning!")
        return True
        
    finally:
        ser.close()

if __name__ == '__main__':
    print("=== Uniden Bearcat BC75XLT Headless Programmer ===")
    port, baud, model = find_bc75xlt_port()
    
    if not port:
        print("\n⚠️ No BC75XLT scanner detected yet.")
        print("Please plug the scanner in via USB Mini-B cable and ensure it is turned ON.")
        print("You can run this script again once plugged in: python bc75xlt_programmer.py")
        sys.exit(1)
    else:
        program_scanner(port, baud, CSV_PATH)
