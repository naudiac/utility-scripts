# ADB Wallpaper Control — Research Notes
**Device:** Samsung Galaxy S24 Ultra (One UI, Android 14/15)  
**Date Tested:** 2026-06-18  
**ADB Connection:** Wi-Fi over LAN, port auto-discovered via port scan (30000–47000 range)  
**ADB IP:** `192.168.4.83`  
**Open ADB Ports Found:** `33251`, `44387` (44387 is the active wireless debugging port)

---

## `cmd wallpaper` — What's Exposed

The `cmd wallpaper` interface on Android 14/15 exposes **only 3 commands**, none of which can set an image:

```bash
adb shell cmd wallpaper help
adb shell cmd wallpaper set-dim-amount <0.0–1.0>   # ✅ WORKS SILENTLY
adb shell cmd wallpaper get-dim-amount              # ✅ WORKS SILENTLY
adb shell cmd wallpaper dim-with-uid <UID> <DIMMING>
```

### Dim Command — Confirmed Working (Silent)
```bash
# Dim wallpaper to 50%
adb shell cmd wallpaper set-dim-amount 0.5

# Revert to normal
adb shell cmd wallpaper set-dim-amount 0.0
```
Output: `Dimming the wallpaper to: 0.5`  
✅ **Executes silently — no UI popup, no user interaction required.**  
⚠️ **Does NOT set a new wallpaper image** — only dims/brightens the existing one.

---

## `service call wallpaper` — Low-Level AIDL

The wallpaper service is registered as service index **471**:
```
471  wallpaper: [android.app.IWallpaperManager]
```

### Method 1 — `setWallpaper` (requires wallpaper category)
```bash
adb shell service call wallpaper 1
```
Returns error: `"Must specify a valid wallpaper category to set"`  
This is the `setWallpaper()` method. It requires a valid `FileDescriptor` and category passed as Parcel data — **not feasible from a raw shell command** without a helper app or script to construct the Parcel binary.

### Why `service call` Can't Practically Set a Wallpaper
- AIDL transaction indices shift between Android versions — method 1 on Android 14 may not be method 1 on Android 15.
- The `setWallpaper` method requires a `ParcelFileDescriptor` (a file handle), which cannot be passed as a shell argument.
- Samsung One UI may overlay additional restrictions on top of AOSP.
- **Verdict: Not viable without a compiled app or root.**

---

## `settings put` — Accessibility Workarounds

### Color Inversion (Changes all colors including icons)
```bash
adb shell settings put secure accessibility_display_inversion_enabled 1   # enable
adb shell settings put secure accessibility_display_inversion_enabled 0   # disable
```
✅ Works silently but **inverts ALL screen colors** — icons, wallpaper, everything. Not a wallpaper change.

### Dark Mode Toggle
```bash
adb shell cmd uimode night yes    # enable dark mode
adb shell cmd uimode night no     # disable dark mode
```
✅ Works silently. Changes system-wide dark mode.

---

## Summary Table

| Action | Command | Works? |
|---|---|---|
| Set new wallpaper image | `service call wallpaper 1 ...` | ❌ Requires binary Parcel FD |
| Set wallpaper via intent | `am start -a android.intent.action.ATTACH_DATA` | ⚠️ Opens UI picker on phone |
| Dim/brighten wallpaper | `cmd wallpaper set-dim-amount 0.0–1.0` | ✅ Silent |
| Invert all colors | `settings put secure accessibility_display_inversion_enabled` | ✅ Silent (whole screen) |
| Dark mode toggle | `cmd uimode night yes/no` | ✅ Silent |

---

## Conclusion

**There is no pure ADB shell command to silently set a new wallpaper image on Android 14/15 without a helper app.**

The `cmd wallpaper` interface intentionally limits what can be done over the shell. The low-level `service call wallpaper` approach requires binary Parcel construction, which is impractical from a command line.

**Recommended Path:** Use **Termux + Termux:API** (`termux-wallpaper -f <path>`) which provides a proper CLI bridge to Android's `WallpaperManager` API — the correct, stable, public interface.

---

## ADB Connection Notes

The wireless debugging port changes each session. A port scan (30000–47000) reliably discovers it.  
Port scanner script: `scan_ports.py` in the brain scratch folder.  
The `phone.ps1` CLI toolkit handles reconnection automatically.
