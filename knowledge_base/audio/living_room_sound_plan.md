# 🔊 Living Room Sound System Plan

**Budget:** $300–$600 | **Config:** 2.1 Stereo | **Use:** Movies + Music equally  
**Connection:** HDMI ARC → Samsung TU7000 | **Placement:** TV stand shelf  
**Goal:** AGY-controllable alongside the TV

---

## ⭐ Recommended Setup — WiiM Amp + Bookshelf Speakers + Sub

This combo hits every requirement: HDMI ARC, AGY-controllable via API, clean shelf footprint, and audiophile-quality sound for both movies and music.

### Components

| Item | Price | Purpose |
|---|---|---|
| **WiiM Amp** | $299 | The brain — HDMI ARC, Wi-Fi, Alexa, API |
| **Polk Audio T15** (pair) | $80 | Budget passive bookshelves, punch above their price |
| **Klipsch R-100SW Subwoofer** | $149 | 10" powered sub, line-level input from WiiM |
| **HDMI ARC cable** | $15 | TV → WiiM Amp |

**Total: ~$543**

---

## Why WiiM Amp is the Key Piece

- ✅ **HDMI ARC input** — TV remote controls volume automatically
- ✅ **Wi-Fi streaming** — AirPlay 2, Spotify Connect, Tidal, Amazon Music
- ✅ **REST API** — fully controllable by AGY
- ✅ **SmartThings integration** — works alongside the Samsung TV
- ✅ **Subwoofer output** — dedicated LFE/line-level sub output
- ✅ **60W × 2** — plenty for a living room

---

## AGY Control (WiiM API)

```powershell
$wiim = "http://192.168.4.XX"
Invoke-RestMethod "$wiim/httpapi.asp?command=setPlayerCmd:vol:40"
Invoke-RestMethod "$wiim/httpapi.asp?command=setPlayerCmd:mute:1"
Invoke-RestMethod "$wiim/httpapi.asp?command=setPlayerCmd:switchmode:HDMI"
```

---

## Connection Diagram

```
Samsung TU7000 TV
    │  HDMI ARC
    ▼
 WiiM Amp ──── speaker wire ────► Left Speaker (Polk T15)
    │           speaker wire ────► Right Speaker (Polk T15)
    │  RCA sub out
    ▼
 Klipsch R-100SW Subwoofer
```

---

## Phased Purchase

- Phase 1 (~$299): WiiM Amp only
- Phase 2 (~$80): Add Polk T15 speakers
- Phase 3 (~$149): Add Klipsch sub

## Shopping Links

| Item | Link |
|---|---|
| WiiM Amp | [Amazon](https://www.amazon.com/s?k=WiiM+Amp) |
| Polk Audio T15 | [amazon.com/dp/B0027D7Y5O](https://www.amazon.com/dp/B0027D7Y5O) |
| Klipsch R-100SW | [amazon.com/dp/B07FKH9ZDC](https://www.amazon.com/dp/B07FKH9ZDC) |
