---
name: samsung-tv-smartthings
description: >
  Control William's Samsung TU7000 65" living room TV via the SmartThings cloud API.
  Use when asked to change volume, mute, power on/off, switch inputs, change channels,
  or get the TV's current status. Also covers the initial pairing workflow if ever
  needed again.
---

# Samsung TV — SmartThings Control

## Credentials (saved 2026-07-08)

| Field | Value |
|---|---|
| SmartThings PAT | `<REDACTED_SMARTTHINGS_PAT>` |
| Device ID | `cc6c7a3a-74cc-16eb-14eb-83267b2b27a2` |
| Device Name | Living room television |
| Model | Samsung UN65TU7000BXZA (65" 4K TU7000, 2020) |
| TV IP (WiFi) | `192.168.4.44` |
| TV IP (Ethernet) | `192.168.4.30` |

## Rate Limits

SmartThings allows **~10 commands per minute** per token.
- Use `setVolume` (1 call) instead of `volumeUp` x N (N calls)
- Space commands at least **7 seconds apart** in loops
- If rate-limited (`TooManyRequestError`), wait 60 seconds before retrying

## Quick Control (PowerShell)

```powershell
$h = @{ Authorization = "Bearer <REDACTED_BEARER_TOKEN>"; "Content-Type" = "application/json" }
$d = "cc6c7a3a-74cc-16eb-14eb-83267b2b27a2"
$api = "https://api.smartthings.com/v1/devices/$d/commands"

# Get full status
Invoke-RestMethod "https://api.smartthings.com/v1/devices/$d/status" -Headers $h

# Volume — set absolute level 0-100 (1 API call, rate-limit friendly)
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"audioVolume","command":"setVolume","arguments":[30]}]}'

# Mute / Unmute
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"audioMute","command":"mute"}]}'
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"audioMute","command":"unmute"}]}'

# Power off / on
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"switch","command":"off"}]}'
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"switch","command":"on"}]}'

# Switch to Fire TV stick (HDMI1) or Live TV (dtv)
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"samsungvd.mediaInputSource","command":"setInputSource","arguments":["HDMI1"]}]}'
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"samsungvd.mediaInputSource","command":"setInputSource","arguments":["dtv"]}]}'

# Set channel by number
Invoke-RestMethod $api -Method Post -Headers $h -Body '{"commands":[{"component":"main","capability":"tvChannel","command":"setTvChannel","arguments":["1170"]}]}'
```

## Known Inputs

| ID | Label |
|---|---|
| `dtv` | Live TV (antenna/cable) |
| `HDMI1` | Amazon Fire TV stick |

## Available Picture Modes
`Dynamic`, `FILMMAKER MODE`, `Movie`, `Natural` (default), `Standard`

## Available Sound Modes
`Adaptive Sound`, `Amplify`, `Standard` (default)

## Initial Pairing Workflow (if ever needed again)

1. On TV: **Settings → General → Sign In** with a Samsung account
2. On phone: Open **SmartThings app → + → Scan nearby**
3. Select **[TV] Samsung TU7000 65 TV** (the entry with the `[TV]` prefix)
4. If "Reset the device" prompt appears: tap **Reset** — this only clears SmartThings cloud registration, NOT TV picture/app/channel settings
5. Get a Personal Access Token: **account.smartthings.com/tokens** → Generate → check all Device scopes → copy immediately (shown once only)
6. Find Device ID: `Invoke-RestMethod "https://api.smartthings.com/v1/devices" -Headers @{ Authorization = "Bearer TOKEN" }`

## Local WebSocket API (reference only — unreliable on this network)

- Port 8001 (ws) / 8002 (wss)
- Endpoint: `ws://192.168.4.44:8001/api/v2/channels/samsung.remote.control?name=BASE64_APP_NAME`
- Auth: `TokenAuthSupport: true` on this TV — requires approval popup + token handshake
- **Known issue**: TV firmware closes the WebSocket with `ms.channel.unauthorized` before the
  popup approval window is actionable, even from the same /24 subnet. Prefer SmartThings.
- Developer Mode: currently ON (set 2026-07-08) — reversible via Smart Hub → Apps → type `12345`
- Access Notification: set to "Always" (Device Connection Manager)
