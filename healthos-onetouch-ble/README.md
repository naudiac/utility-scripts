# HealthOS — OneTouch Blood Sugar Import

AGY skill for importing blood glucose readings from the **OneTouch Verio Reflect** meter into HealthOS via ADB screen extraction.

## Background

Two methods were attempted before landing on the current working approach:

| Method | Status | Reason |
|--------|--------|--------|
| **PC Bluetooth LE (Bleak)** | ❌ Retired | Meter pairing protocol not reliably reverse-engineered; raw BLE notifications inconsistently decoded |
| **OneTouch Reveal OAuth API** | ❌ Retired | OAuth token flow broken / app API not publicly accessible |
| **ADB UI Screen Extraction** | ✅ Active | Reliably reads logbook data directly from the OneTouch Reveal Android app via `uiautomator` XML dump |

## How It Works

1. **Launch** the OneTouch Reveal app on the phone via ADB `monkey` intent
2. **Wait 30 seconds** for the meter to auto-sync over Bluetooth to the app
3. **Dump the UI hierarchy** with `adb shell uiautomator dump` → pulls XML to PC
4. **Parse readings** from `tv_value` (mg/dL) and `tv_date_time` nodes in the XML
5. **Determine meal type** via MCP `android-adb/screenshot` (visual inspection only — confirmed that `iv_meal_status` ImageView carries **zero text/content-desc data** in the XML; meal icon is purely visual)
6. **De-duplicate** against existing `glucose_log.json` entries
7. **Append new entries** to `glucose_log.json` and `health_journal.json`
8. **Janitor cleanup** — kill app, delete temp XML dump

## Key Findings (XML Schema)

- `com.lifescan.reveal:id/tv_value` — glucose value (e.g. `"180\u00a0"`, trailing U+00A0 non-breaking space on every reading regardless of meal type)
- `com.lifescan.reveal:id/tv_unit_of_measure` — always `"mg/dL"`
- `com.lifescan.reveal:id/tv_date_time` — timestamp (e.g. `"Today, 09:09"` or `"Yesterday, 22:01"`)
- `com.lifescan.reveal:id/iv_meal_status` — ImageView, **always empty `content-desc` and `text`**. Meal icon is visual-only; must use MCP screenshot to read it.
- `com.lifescan.reveal:id/iv_event_icon` — similarly empty

## Meal Icon Detection

The `iv_meal_status` node provides **no parseable XML data**. The only reliable method:

```
mcp tool: android-adb / screenshot
arguments: { "deviceId": "192.168.4.83:39909" }
```

Visual mapping:
| Icon | Description | `type` value |
|------|-------------|-------------|
| 🍎 | Whole apple (filled) | `premeal` |
| 🍏 | Apple core (eaten) | `postmeal` |
| *(none)* | No icon | `random` |

> ⚠️ **Do NOT** pull a local PNG and call `view_file` on it — this crashes the AGY CLI regardless of model tier. The MCP tool result is self-contained and complete.

## ADB Device Setup

```powershell
$adb = "...\platform-tools\adb.exe"
& $adb connect 192.168.4.83:39909
& $adb devices  # must show exactly ONE device to avoid "more than one device" errors
```

> If `adb devices` shows two entries for the same phone (TCP + mDNS pairing), disconnect the mDNS one:
> ```powershell
> & $adb disconnect "adb-R5CX50A4S8Z-vYUihn._adb-tls-connect._tcp"
> ```

## Output Files

| File | Description |
|------|-------------|
| `HealthOS/data/glucose_log.json` | Primary blood sugar log |
| `HealthOS/data/health_journal.json` | Daily health journal with glucose timeline |

## AGY Skill

Implemented as `healthos-onetouch-bs-import` skill in:
```
C:\Users\whanusiewicz\.gemini\config\skills\healthos-onetouch-bs-import\SKILL.md
```

Trigger phrase: **"update my blood sugar"**