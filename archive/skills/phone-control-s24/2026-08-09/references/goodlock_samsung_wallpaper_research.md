# Good Lock & Samsung Wallpaper Modules — ADB Research Notes
**Device:** Samsung Galaxy S24 Ultra (One UI, Android 14/15)  
**Date Tested:** 2026-06-18

---

## Installed Relevant Packages Found on Device

| Package | Purpose |
|---|---|
| `com.samsung.android.goodlock` | Good Lock main shell/launcher |
| `com.samsung.android.themestore` | Galaxy Themes store |
| `com.samsung.systemui.lockstar` | LockStar (lock screen customization) |
| `com.samsung.android.multistar` | MultiStar (multi-window) |
| `com.samsung.android.wallpaper.live` | Samsung live/animated wallpapers |
| `com.android.wallpapercropper` | AOSP wallpaper cropper |
| `com.android.wallpaper.livepicker` | Live wallpaper picker |
| `com.google.android.apps.aiwallpapers` | Google AI Wallpapers |
| `com.samsung.android.wallpaper.res` | Samsung wallpaper resources |
| `com.samsung.android.themecenter` | Theme Center |

> [!NOTE]
> `Home Up` (`com.samsung.android.app.homescreen.gutshot`) was **not found** on this device. It may not be installed or may be bundled differently in this One UI version.

---

## Good Lock (`com.samsung.android.goodlock`) — Exported Receivers

Only infrastructure/framework receivers found — **none useful for wallpaper control:**
- `androidx.profileinstaller.ProfileInstallReceiver` — JIT profile installer
- `.data.account.AccountSignOutReceiver` — account management
- `.ui.LocaleChangeReceiver` — locale changes
- `.ui.appwidget.cassette.CassetteAppWidgetReceiver` — widget updates
- `androidx.work.impl.diagnostics.DiagnosticsReceiver` — WorkManager diagnostics

**Verdict:** Good Lock shell exposes no wallpaper-related broadcast hooks.

---

## LockStar (`com.samsung.systemui.lockstar`) — Exported Receivers

Only infrastructure receivers:
- `androidx.profileinstaller.ProfileInstallReceiver`
- `.data.backup.BackupAndRestoreReceiver` — backup/restore only

**Verdict:** No wallpaper control hooks accessible via ADB broadcasts.

---

## Samsung Live Wallpaper (`com.samsung.android.wallpaper.live`) — Services Found

This is the most interesting package. It exposes **WallpaperService** entries bound under:

```
Action: "com.samsung.android.service.wallpaper.LiveWallpaperService"
Action: "com.samsung.android.service.wallpaper.CoverWallpaperService"
```

### Available Live Wallpaper Services (bind targets):
| Class | Type |
|---|---|
| `.layered.LayeredWallpaperService` | Layered animated wallpaper |
| `.unified.UnifiedWallpaperService` | Unified wallpaper |
| `.graphical.GraphicalWallpaperService` | Graphical/rendered wallpaper |
| `.dailygradient.DailyGradientWallpaperService` | Daily gradient |
| `.liveeffect.LiveEffectService` | Live effect layer |
| `.weather.effects.WeatherWallpaperService` | Weather-reactive wallpaper |
| `.tiltclock.TiltClockWallpaperService` | Tilt clock (cover screen) |

All are bound with `permission: android.permission.BIND_WALLPAPER` — **cannot be triggered from shell without this permission.**

### ADB Command to Switch to a Samsung Live Wallpaper (via `setWallpaperComponent`):
```bash
adb shell cmd wallpaper set-dim-amount 0.0  # works (dim only)

# Switch to Daily Gradient live wallpaper (requires BIND_WALLPAPER perm — needs helper app or root):
adb shell am start -a android.intent.action.SET_WALLPAPER  # opens picker (not silent)
```

**Verdict:** Samsung live wallpaper services are **all permission-gated** with `BIND_WALLPAPER`. Cannot be directly activated from ADB shell without either root or a signed/privileged app.

---

## Summary: Good Lock / Samsung Wallpaper via ADB

| Capability | Feasible from ADB? | Notes |
|---|---|---|
| Dim existing wallpaper | ✅ Yes | `cmd wallpaper set-dim-amount` |
| Switch to Samsung live wallpaper | ❌ No | Requires `BIND_WALLPAPER` permission |
| Set static image wallpaper | ❌ No | No shell API without app |
| Control Good Lock modules | ❌ No | No exported broadcast receivers |
| Control LockStar | ❌ No | Only backup receiver exposed |

---

## Final Conclusion

**Good Lock and Samsung's wallpaper ecosystem are fully closed to standard ADB automation.** All meaningful actions require either:
1. The `BIND_WALLPAPER` system permission (granted only to privileged/signed apps)
2. Root access
3. A helper app using Android's public `WallpaperManager` API

**→ Proceed with Termux + Termux:API (Option A)** — this is the correct, clean, and supported path for CLI-driven wallpaper control.
