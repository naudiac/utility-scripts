# Baofeng BF-F8HP Hardware Limits & Specification Reference

## Transceiver Architecture

The Baofeng BF-F8HP is a dual-band handheld FM transceiver based on direct-conversion DSP architecture.

### Key Hardware Parameters

| Parameter | Limit / Specification | Notes |
|:----------|:----------------------|:------|
| **Memory Channels** | Exactly 128 (Slots `0` to `127`) | Hard EEPROM limit. Attempting to program slot 128+ causes memory corruption. |
| **VHF Frequency Range** | `136.0000 MHz` – `174.0000 MHz` | RX and TX (Subject to FCC licensing & band plan). |
| **UHF Frequency Range** | `400.0000 MHz` – `520.0000 MHz` | RX and TX (Commercial/Ham/GMRS spectrum). |
| **220 MHz Band** | Unsupported | BF-F8HP cannot transmit or receive in the 1.25m (222-225 MHz) band. |
| **Channel Name Length** | Maximum 7 Characters | Alphanumeric only (`A-Z`, `0-9`, `-`, space). |
| **RF Power Levels** | High: ~8 Watts, Med: ~4 Watts, Low: ~1 Watt | 3-tier selectable output power. |
| **Modulation Modes** | Wide FM (25 kHz), Narrow FM (12.5 kHz) | NFM required on FRS/GMRS interstitial channels. |
| **Tuning Steps** | `2.5`, `5.0`, `6.25`, `10.0`, `12.5`, `25.0 kHz` | Configurable per channel or in VFO mode. |
| **CTCSS Tones** | 50 Standard EIA Sub-audible Tones | `67.0 Hz` through `254.1 Hz`. |
| **DCS Digital Codes** | 104 Standard Digital Codes | `D023N` through `D754I` (Normal & Inverted). |
| **Memory Image Size** | `0x1808` bytes (6,152 bytes) | Standard binary EEPROM image footprint. |

---

## Memory Map Layout in EEPROM

1. **Channel Frequency Table (`0x0008` – `0x0807`)**:
   - 128 memory slots × 16 bytes per channel.
   - Frequency encoded as 4-byte Little-Endian BCD in 10 Hz units.
2. **Channel Name Table (`0x1000` – `0x1800`)**:
   - 128 memory slots × 16 bytes per channel name.
   - ASCII text padded with `0xFF` or `0x00`, truncated to 7 display characters.
3. **Radio Settings Block (`0x0E20` – `0x0EC0`)**:
   - Squelch level (0-9), VOX sensitivity, timeout timer (TOT), voice prompt language, beep flags, display backlight colors.
