# 🎛️ Mobile DJ Rig — Master Plan

**Style:** Dawless techno live rig + DJ playback  
**Scale:** Outdoor/indoor, 50-100 people  
**Transport:** Van/trailer + wheeled road cases  
**Power:** Wall primary + deep cycle battery backup

---

## Equipment Owned ✅

| Gear | Role |
|---|---|
| Denon DJ Prime Go | Main DJ deck — 2-deck standalone, XLR master out |
| Mackie ProFX8v2 | Master mixer — sums synths + Prime Go |
| Hardware synths + drum machines (Elektron, Roland, Moog-style) | Live instruments |
| 4× Wolfenhag 12" subs + 2 boxes | Low end |
| AudioBahn car speakers | Mids / highs (tops) |
| Car amplifiers (brand TBD) | Power for subs + tops |
| XLR cables, power strips, extension cords | Signal + power |

---

## Signal Flow

```
Hardware Synths / Drum Machines
        │ XLR / TRS per instrument
        ▼
┌──────────────────┐
│  Mackie ProFX8v2 │◄── Prime Go Master Out (XLR)
└────────┬─────────┘
         │ XLR Main Out → XLR/RCA adapter
         ▼
    Car Amp(s)  [built-in crossover]
         ├── Low-pass → Wolfenhag 12" sub boxes
         └── High-pass → AudioBahn tops on stands
```

---

## Power Architecture

```
Wall Outlet
    ├──► 12V DC Power Supply (per amp) ──► Car Amps
    └──► Power Strip ──► Prime Go, Mackie, Synths

Deep Cycle Battery (12V backup)
    └──► Car Amps (manual switch or auto-failover)
```

---

## Scenario A — Full Independent DJ Rig
*(All car audio dedicated to DJ rig; living room uses new gear)*

- All 4 Wolfenhag subs (both boxes)
- All AudioBahn tops
- All amps
- 2× 12V DC PSUs + 1 deep cycle battery

**Pros:** Maximum power, no conflicts  
**Cons:** Living room needs new sub + speakers (~$249)

---

## Scenario B — Shared Gear (Recommended)
*(1 sub box + 1 amp pair shared with living room)*

| Component | Living Room | DJ Rig |
|---|---|---|
| Wolfenhag sub box | 1 box (2 subs) | 1 box (2 subs) |
| AudioBahn speakers | 1 stereo pair | Remaining |
| Car amp | 1 | Remaining |

**Pros:** Saves most money, both systems work  
**Cons:** DJ deployment temporarily removes living room sub

---

## Items to Buy

| Item | Est. Price |
|---|---|
| XLR to RCA adapters (pair) | ~$10 |
| 12V DC Power Supply, 30A (per amp) | ~$45 each |
| Deep cycle battery, 12V group 27 | ~$120 |
| Battery terminals + 4ga power wire | ~$25 |
| Speaker stands (pair) | ~$50–80 |
| Behringer HD400 Hum Destroyer (optional) | ~$30 |

---

## Event Day Setup Order

1. Power — extension cords, 12V PSUs or battery
2. Sub boxes — position, connect to amp
3. Speaker stands — AudioBahn tops at ear height
4. DJ table — Prime Go + Mackie side by side
5. Synths — XLR/TRS into Mackie ch 1–6
6. Prime Go → Mackie ch 7/8
7. Mackie → Car amps (XLR/RCA)
8. Soundcheck — set crossover ~80Hz
9. Gain structure — Mackie at 0dB, trim amp gain

## Teardown (Reverse)
1. Power off amps first
2. Coil cables (signal → power)
3. Pack synths, stands, subs, Mackie, Prime Go

---

## Future Upgrades

| Upgrade | Why |
|---|---|
| Tascam Model 2400 | Replaces Mackie for studio + live |
| Pioneer CDJ-3000 / XDJ-RX3 | Upgrades Prime Go for larger venues |
| QSC K12.2 or RCF powered tops | Replace AudioBahn car speakers |
| Road cases (Pelican/SKB) | Full transport protection |

---

## Note on AudioBahn as PA Tops

Car speakers need enclosures to perform correctly outdoors. Simple ported wooden boxes or open-baffle mounts will work. Impedance is typically 4Ω — compatible with car amps. Confirm power handling once amp model is identified.
