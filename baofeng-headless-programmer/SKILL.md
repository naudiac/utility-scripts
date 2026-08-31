---
name: baofeng-headless-programmer
description: Automates reading, modifying, and writing Baofeng BF-F8HP radio configurations headlessly via CHIRP CLI and dynamic frequency sourcing (NOAA, RepeaterBook, GMRS, Simplex).
---

# Baofeng BF-F8HP Headless Programmer Skill

The `baofeng-headless-programmer` skill provides fully automated, headless radio memory reading, dynamic frequency sourcing, intelligent channel layout merging, and safe writeback for Baofeng BF-F8HP and UV-5R hand-held transceivers using the CHIRP command-line tools (`chirpc`).

## Key Capabilities

1. **Headless Radio Interface**: Connects directly to the radio over serial COM ports, downloads live binary memory images (`.img`), and creates timestamped backups before performing any modifications.
2. **Dynamic Frequency Sourcing**: Automatically resolves US Zip Codes to geographic coordinates via Zippopotam, queries active amateur repeaters within a specified radius (e.g. 35 miles), and pulls NOAA weather frequencies.
3. **Emergency & Utility Spectrum Synthesis**: Injects the National VHF Simplex Calling frequency (146.520 MHz), all 22 standard GMRS/FRS channels, and all 7 NOAA weather radio frequencies (with transmit-inhibit safety enabled).
4. **Strict Quality & Priority Filtering**: Filters repeater datasets to strictly include verified "On-Air" repeaters, ranking emergency communications infrastructure (ARES, RACES, SKYWARN, and linked wide-area repeater networks) at the highest priority.
5. **Hardware Limit Enforcement**: Strictly adheres to the Baofeng BF-F8HP hardware limits: exactly 128 memory channels (slots 0..127), 7-character alphanumeric LCD display names, supported VHF (136-174 MHz) / UHF (400-520 MHz) frequency bands, standard 50 CTCSS tones, and DCS digital squelch codes.
6. **Safe Headless Writeback**: Writes the updated memory configuration back to the radio via `chirpc` and verifies image integrity without opening GUI windows or prompting for user confirmation.

---

## Architecture & Data Flow

```
                                  ┌───────────────────────────────┐
                                  │      User / Agent Request     │
                                  │  (Zip: 30445, Port: COM3)     │
                                  └───────────────┬───────────────┘
                                                  │
                                                  ▼
                                  ┌───────────────────────────────┐
                                  │    baofeng_programmer.py      │
                                  │       (CLI Entrypoint)        │
                                  └───────────────┬───────────────┘
                                                  │
                ┌─────────────────────────────────┼─────────────────────────────────┐
                │                                 │                                 │
                ▼                                 ▼                                 ▼
    ┌───────────────────────┐         ┌───────────────────────┐         ┌───────────────────────┐
    │    chirp_driver.py    │         │ frequency_fetcher.py  │         │     csv_engine.py     │
    │  - chirpc subprocess  │         │  - Zip Geocoder       │         │  - 19/21-col CHIRP CSV│
    │  - Timestamped backup │         │  - RepeaterBook API   │         │  - 7-char tag sanitize│
    │  - Mock / Dry-Run sim │         │  - NOAA / GMRS synth  │         │  - 128-ch allocator   │
    │  - Image validation   │         │  - EmComm rank & sort │         │  - Channel merger     │
    └───────────┬───────────┘         └───────────┬───────────┘         └───────────┬───────────┘
                │                                 │                                 │
                └─────────────────────────────────┼─────────────────────────────────┘
                                                  ▼
                                      ┌───────────────────────┐
                                      │       models.py       │
                                      │ ChannelEntry, Repeater│
                                      │ GeoLocation, Subproc  │
                                      └───────────────────────┘
```

---

## Memory Channel Allocation Layout

When synthesizing a fresh frequency plan for a target zip code, channels are organized into a logical tiered structure:

| Memory Channel Slots | Allocation Type | Details | Transmit Power | Duplex / Tone |
|:--------------------:|:----------------|:--------|:--------------:|:--------------|
| **0** | National Simplex Calling | `146.5200 MHz` (2m Simplex) | High (8W) | Simplex (Duplex: `""`) |
| **1 .. N** | Local Amateur Repeaters | Prioritized On-Air repeaters (ARES, Linked, SKYWARN, Club) | High (8W) | Standard offset & CTCSS/DCS |
| **N+1 .. N+22** | GMRS / FRS 1-22 | Standard 22 UHF channels (`462.5625 - 467.7250 MHz`) | High (8W) | Simplex |
| **N+23 .. N+29** | NOAA Weather Radio | 7 NOAA stations (`162.400 - 162.550 MHz`) | Low (1W) | RX Only (Duplex: `off`) |

*Total channel count never exceeds 128 slots (0..127).*

---

## CLI Usage & Options

### Primary Syntax
```powershell
python -m baofeng_programmer [COMMAND] [OPTIONS]
```

### Common Flags
- `--zip <ZIP>`: 5-digit US Postal Zip Code (e.g. `30445`).
- `--port <PORT>`: Serial programming COM port (e.g. `COM3`, `/dev/ttyUSB0`).
- `--radio-model <MODEL>`: CHIRP radio identifier (default: `Baofeng_BF-F8HP`).
- `--output-csv <PATH>`: Destination path for exported CHIRP CSV.
- `--backup-dir <PATH>`: Directory for storing timestamped `.img` backups (default: `./backups`).
- `--radius <MILES>`: Search radius in miles for repeater discovery (default: `35.0`).
- `--bands <BANDS>`: Comma-separated target bands (e.g. `2m,70cm`).
- `--power <LEVEL>`: Default power level (`High`, `Med`, `Low`).
- `--start-channel <INDEX>`: Starting channel index for repeaters (default: `1`).
- `--max-channels <COUNT>`: Maximum channel limit (default: `128`).
- `--dry-run`: Simulate subprocess execution without communicating with physical serial ports.
- `--mock`: Use offline deterministic fixtures and synthetic memory images.
- `--json`: Output execution status and diagnostics in structured JSON.
- `--verbose`, `-v`: Enable verbose debug logging.
- `--token <TOKEN>`: Optional RepeaterBook API authentication token.

---

## Usage Examples

### 1. Full Automated Read-Merge-Write Pipeline
Download existing image, backup, fetch local frequencies for zip 30445, synthesize plan, and write to radio on COM3:
```powershell
python "C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer\scripts\baofeng_programmer.py" --zip 30445 --port COM3 --backup-dir ./backups
```

### 2. Standalone CSV Plan Generation (Fetch-Only)
Generate a CHIRP-compatible CSV file for Metter, GA without connecting a radio:
```powershell
python "C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer\scripts\baofeng_programmer.py" fetch --zip 30445 --output-csv ./metter_plan.csv
```

### 3. Headless Radio Backup (Download-Only)
Download the current memory image from the radio and save a timestamped backup:
```powershell
python "C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer\scripts\baofeng_programmer.py" download --port COM3 --backup-dir ./backups
```

### 4. CI / Deterministic Testing Simulation (Mock & Dry-Run)
Simulate full programming in CI without physical serial hardware or external network calls:
```powershell
python "C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer\scripts\baofeng_programmer.py" --zip 30445 --port COM3 --dry-run --mock --json
```

---

## Exit Codes

| Exit Code | Identifier | Description |
|:---------:|:-----------|:------------|
| `0` | `EXIT_SUCCESS` | Operation completed successfully. |
| `1` | `EXIT_GENERAL_ERROR` | Unhandled exception or CSV validation failure. |
| `2` | `EXIT_COM_PORT_ERROR` | Serial communication error, timeout, or CHIRP subprocess failure. |
| `3` | `EXIT_API_ERROR` | Geocoding or repeater sourcing failure (invalid zip or API error). |
| `4` | `EXIT_CAPACITY_OVERFLOW` | Memory channel limit exceeded (> 128 channels). |

---

## Troubleshooting & Best Practices

1. **CHIRP CLI Availability**: Ensure `chirpc` is installed and accessible on your system PATH, or provide mock/dry-run options when testing in isolated environments.
2. **Serial Cable Drivers**: On Windows, ensure FTDI / Prolific USB-to-Serial drivers are installed and the COM port is visible under Device Manager. The BF-F8HP cable uses a **CH340** chip — COM port belongs to the cable, not the radio. Unplugging the USB cable changes the port, but power-cycling the radio does NOT.
3. **Radio Volume / Power**: Ensure the radio is powered ON and volume is set to ~50-70% prior to reading or writing.
4. **Backup Preservation**: Backups are saved with microsecond/second ISO timestamp prefixes (`backup_Baofeng_BF-F8HP_YYYYMMDD_HHMMSS.img`). Never delete these backups until radio operation is verified in the field.

---

## Critical Lessons Learned (2026-08-31 Field Session)

### CHIRP CLI Is Unreliable — Use the Python API Directly
The `chirpc` command-line wrapper cannot merge CSV data into a radio image. It only downloads and re-uploads the same unmodified `.img` file. **Bypass the CLI entirely** and use the CHIRP Python API directly:

```python
import os, serial
os.environ['CHIRP_TESTENV'] = '1'  # CRITICAL: prevents CHIRP logger from hijacking stdout

from chirp.drivers.uv5r import BaofengUV5R
from chirp import chirp_common, directory
directory.import_drivers()

ser = serial.Serial(r'\\.\COM10')
radio = BaofengUV5R(ser)
radio.sync_in()        # Download from radio
# OR: radio.load_mmap('backup.img')  # Load from cached file (avoids Clone Mode)

mem = chirp_common.Memory()
mem.number = 0
mem.freq = 146520000   # Frequency in Hz
mem.name = 'CALL2M'    # Max 7 chars
mem.duplex = ''        # '', '-', '+', 'off'
mem.offset = 0
mem.tmode = 'Tone'     # '', 'Tone', 'TSQL'
mem.rtone = 100.0
mem.mode = 'FM'        # 'FM', 'NFM'
radio.set_memory(mem)

radio.sync_out()       # Upload to radio
ser.close()
```

### Clone Mode Lockout
After `radio.sync_in()`, the BF-F8HP physically locks into "Clone Mode" (LCD shows `CLONE`). A subsequent `sync_out()` on the same serial session will **fail** with `RadioNoContactLikelyK1`. Two solutions:
1. **Power cycle the radio** (twist volume knob off/on) — the COM port stays active because it belongs to the CH340 USB cable, not the radio
2. **Use `radio.load_mmap()`** to load a cached `.img` file from disk instead of downloading. This skips Clone Mode entirely and allows an immediate `sync_out()`

### The Optimal Upload-Only Strategy
For fastest programming, use a two-phase approach:
1. **Phase 1 (one-time):** `sync_in()` to download and save a baseline `.img` file
2. **Phase 2 (every update):** `load_mmap()` → merge channels → `sync_out()` — no download needed, no Clone Mode, instant upload

### CHIRP Logger Hijack
CHIRP's `logger.py` detects headless/non-TTY execution and forcefully redirects `sys.stdout` and `sys.stderr` to `%APPDATA%\CHIRP\debug.log`. This causes the script to appear to produce no output and silently exit with code 0. **Fix:** Set `os.environ['CHIRP_TESTENV'] = '1'` before any CHIRP imports.

### Serial Port Safety
Always wrap radio operations in `try/finally` with `ser.close()`. If the serial port isn't properly closed after an exception, the CH340 driver locks the COM port, resulting in `PermissionError(13, 'Access is denied.')` on all subsequent attempts until the Python process dies.

### CSV Parsing
The skill's `CSVEngine` / `CSVRadio` parser rejects `High`/`Low` power strings passed as raw text. For reliable channel loading, use Python's standard `csv.DictReader` to parse the CSV and construct `chirp_common.Memory()` objects directly.

---

## Live Reference Website

A companion GitHub Pages site is deployed at:
**https://naudiac.github.io/utility-scripts/baofeng-scanner/**

Features: full 128-channel table, print-friendly cheat sheet, channel rating system, I-16/I-75 travel route guides, ISS pass tracker, time-of-day activity guide, CSV download for re-flashing.

---

## Current Active CSV

The latest channel plan is stored at:
`C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer\baofeng_ultimate_30445.csv`

128 channels covering: National simplex, NOAA Weather, Public Safety Interop, Marine VHF, Railroad AAR, ISS, MURS, Business itinerant, GMRS/FRS, and local repeaters from Savannah through Mount Vernon to Atlanta.
