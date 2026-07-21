# HealthOS - OneTouch Verio Reflect Bluetooth LE Direct Sync

## Overview
Documentation for the direct PC Bluetooth LE sync integration for William's **OneTouch Verio Reflect** blood sugar (glucose) meters into HealthOS (`data/glucose_log.json`).

## Device & GATT Details
- **Target Meter Names**: `1JM-US-TBA4290A` (`44:6F:F8:43:F6:00`), `1JM-US-TBA3961A` (`44:6F:F8:43:D7:3A`)
- **Service UUID**: `2dd10010-1c37-452d-8979-d1b4a787d0a4`
- **Write Characteristic (RX)**: `2dd10011-1c37-452d-8979-d1b4a787d0a4`
- **Notify Characteristic (NT)**: `2dd10013-1c37-452d-8979-d1b4a787d0a4`

## Command Protocol & Stream Decoding
1. **Command Framing**: Send ASCII commands with MSB bit set (`b | 0x80`):
   - `RPR\r` (Read Patient Records)
   - `RMR\r` (Read Meter Records)
   - `DMP\r` (Dump Records)
2. **Notification Stream Decoding**:
   - **ASCII Streams**: Mask bytes with `0x7F` and regex parse 2-3 digit integers in the range `40..500`.
   - **Nibble Encodings**: Map characters between `@` and `O` to nibbles `0..15` (`ord(c) - ord('@')`), combine pairs into bytes `(high << 4) | low`, and extract valid glucose values.
