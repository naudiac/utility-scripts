# Frequency Tables & Allocation Standards

This reference documents the canonical frequencies injected by the `baofeng-headless-programmer` frequency synthesizer.

---

## 1. National Simplex Calling Frequency

| Channel Name | Frequency (MHz) | Mode | Duplex | Offset | Power | Purpose |
|:------------|:---------------:|:----:|:------:|:------:|:-----:|:--------|
| `CALL-2M` | `146.5200` | FM | `""` (Simplex) | `0.000` | High | National VHF FM Calling Channel (North America) |

---

## 2. NOAA Weather Radio (NWR) Channels

All NOAA Weather Radio stations operate in transmit-inhibit mode (`Duplex = "off"`, `Power = "Low"`) to prevent accidental transmission on federal weather alert frequencies.

| Channel Name | Frequency (MHz) | Duplex | Mode | Power | Skip | Station Code |
|:------------|:---------------:|:------:|:----:|:-----:|:----:|:------------|
| `WX 1` | `162.5500` | `off` | FM | Low | `""` | WX1 (Standard Primary) |
| `WX 2` | `162.4000` | `off` | FM | Low | `""` | WX2 |
| `WX 3` | `162.4750` | `off` | FM | Low | `""` | WX3 |
| `WX 4` | `162.4250` | `off` | FM | Low | `""` | WX4 |
| `WX 5` | `162.4500` | `off` | FM | Low | `""` | WX5 |
| `WX 6` | `162.5000` | `off` | FM | Low | `""` | WX6 |
| `WX 7` | `162.5250` | `off` | FM | Low | `""` | WX7 |

---

## 3. GMRS / FRS Simplex Channels (1–22)

Standard 22-channel UHF allocation across the 462 MHz and 467 MHz bands.

| Channel # | Channel Name | Frequency (MHz) | Bandwidth | Mode | Default Power |
|:---------:|:------------|:---------------:|:---------:|:----:|:-------------:|
| **1** | `GMRS 1` | `462.5625` | Narrow | NFM | High |
| **2** | `GMRS 2` | `462.5875` | Narrow | NFM | High |
| **3** | `GMRS 3` | `462.6125` | Narrow | NFM | High |
| **4** | `GMRS 4` | `462.6375` | Narrow | NFM | High |
| **5** | `GMRS 5` | `462.6625` | Narrow | NFM | High |
| **6** | `GMRS 6` | `462.6875` | Narrow | NFM | High |
| **7** | `GMRS 7` | `462.7125` | Narrow | NFM | High |
| **8** | `GMRS 8` | `467.5625` | Narrow | NFM | Low |
| **9** | `GMRS 9` | `467.5875` | Narrow | NFM | Low |
| **10** | `GMRS 10` | `467.6125` | Narrow | NFM | Low |
| **11** | `GMRS 11` | `467.6375` | Narrow | NFM | Low |
| **12** | `GMRS 12` | `467.6625` | Narrow | NFM | Low |
| **13** | `GMRS 13` | `467.6875` | Narrow | NFM | Low |
| **14** | `GMRS 14` | `467.7125` | Narrow | NFM | Low |
| **15** | `GMRS 15` | `462.5500` | Wide | FM | High |
| **16** | `GMRS 16` | `462.5750` | Wide | FM | High |
| **17** | `GMRS 17` | `462.6000` | Wide | FM | High |
| **18** | `GMRS 18` | `462.6250` | Wide | FM | High |
| **19** | `GMRS 19` | `462.6500` | Wide | FM | High |
| **20** | `GMRS 20` | `462.6750` | Wide | FM | High |
| **21** | `GMRS 21` | `462.7000` | Wide | FM | High |
| **22** | `GMRS 22` | `462.7250` | Wide | FM | High |

---

## 4. Standard CTCSS Tones (EIA-50 Standard)

The 50 standard continuous tone-coded squelch frequencies (in Hz):

```
67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 159.8, 162.2, 165.5, 167.9,
171.3, 173.8, 177.3, 179.9, 183.5, 186.2, 189.9, 192.8, 196.6, 199.5,
203.5, 206.5, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3, 254.1
```
