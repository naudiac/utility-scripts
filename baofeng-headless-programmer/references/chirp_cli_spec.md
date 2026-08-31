# CHIRP Command-Line Interface (`chirpc`) Specification

## Overview
CHIRP provides a scriptable command-line interface (`chirpc`) designed for headless automation of amateur radio memory reading, configuration, cloning, and writeback.

## Command Syntax

### 1. Download Radio Memory Image (`--download-mmap`)
Downloads raw binary memory map directly from the transceiver over a serial port:
```bash
chirpc -r <RADIO_MODEL> --serial=<PORT> --mmap=<OUTPUT_PATH.img> --download-mmap
```
- `-r <RADIO_MODEL>`: Specifies the radio driver (e.g. `Baofeng_BF-F8HP`, `Baofeng_UV-5R`).
- `--serial=<PORT>`: Specifies the communication port (e.g. `COM3` on Windows, `/dev/ttyUSB0` on Linux/macOS).
- `--mmap=<OUTPUT_PATH>`: Target output file path for the raw binary image.
- `--download-mmap`: Flag instructing CHIRP to execute the serial read routine.

### 2. Upload Radio Memory Image (`--upload-mmap`)
Uploads a binary memory image directly into the radio's EEPROM:
```bash
chirpc -r <RADIO_MODEL> --serial=<PORT> --mmap=<INPUT_PATH.img> --upload-mmap
```
- `--upload-mmap`: Flag instructing CHIRP to write the binary image to the radio EEPROM and verify transmission checksums.

### 3. CSV Import / Export Schema

CHIRP supports standard 19-column and 21-column CSV formats for channel programming.

#### Standard 19-Column Header:
`Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE`

#### Standard 21-Column Header (with Split DCS & Cross Modes):
`Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,RxDtcsCode,CrossMode,Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE`

### Key Field Value Definitions

| Field | Allowed Values | Description |
|:------|:---------------|:------------|
| `Location` | `0 .. 127` | Zero-indexed channel slot number in radio memory. |
| `Name` | Max 7 alphanumeric chars | Display name shown on radio LCD. |
| `Frequency` | Float (MHz) | Receive frequency (e.g. `146.520000`). |
| `Duplex` | `""`, `"+"`, `"-"`, `"off"`, `"split"` | Offset direction. `"off"` disables transmitter (TX Inhibit). |
| `Offset` | Float (MHz) | Transmit offset magnitude (e.g. `0.600000` for 2m, `5.000000` for 70cm). |
| `Tone` | `""`, `"Tone"`, `"TSQL"`, `"DTCS"`, `"Cross"` | Sub-audible squelch mode. `"Tone"` transmits CTCSS; `"TSQL"` requires CTCSS for receive. |
| `rToneFreq` | Float (Hz) | Transmit CTCSS tone frequency (e.g. `100.0`). |
| `cToneFreq` | Float (Hz) | Receive / Squelch CTCSS tone frequency (e.g. `100.0`). |
| `DtcsCode` | 3-digit string (`023` .. `754`) | Digital Coded Squelch code. |
| `DtcsPolarity`| `"NN"`, `"NR"`, `"RN"`, `"RR"` | DCS polarity (Normal/Inverted). |
| `Mode` | `"FM"`, `"NFM"` | Modulation bandwidth (`FM` = 25 kHz wide, `NFM` = 12.5 kHz narrow). |
| `TStep` | Float (kHz) | Tuning step size (`2.5`, `5.0`, `6.25`, `10.0`, `12.5`, `25.0`). |
| `Skip` | `""`, `"S"` | Scan skip flag (`"S"` skips channel during VFO/MR memory scan). |
| `Power` | `"High"`, `"Med"`, `"Low"` | RF output power level. |
