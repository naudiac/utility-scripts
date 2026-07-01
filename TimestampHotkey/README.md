# utility-scripts

Personal collection of Windows utility scripts and automation tools.

---

## TimestampHotkey

**Press `Ctrl+Alt+D` anywhere → instantly copies a timestamp to your clipboard.**

Example output: `2026-07-01_03-48-25`

### How it works

Zero background processes. A Windows Start Menu shortcut (`.lnk`) holds the global hotkey registration via Explorer. When pressed, it calls `wscript.exe` → a one-line VBScript → PowerShell `Get-Date` → clipboard. Everything exits immediately.

### Install

1. Download `TimestampHotkey/Install-TimestampHotkey.ps1`
2. Right-click → **Run with PowerShell**
3. Choose **[1] Install**
4. Sign out and back in once (Explorer re-reads Start Menu hotkeys at login)

### Uninstall

```powershell
.\Install-TimestampHotkey.ps1 -Uninstall
```

Or run the script and choose **[2] Uninstall** from the menu.

### Command-line flags

```powershell
.\Install-TimestampHotkey.ps1 -Install    # silent install
.\Install-TimestampHotkey.ps1 -Uninstall  # silent uninstall
```

### Files installed

| File | Location |
|---|---|
| `SilentTime.vbs` | `Documents\Scripts\SilentTime.vbs` |
| `SilentTime.lnk` | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\` |

### Requirements

- Windows 10 / 11
- PowerShell 5.1+ (built-in)
- No admin rights needed

### Sharing with a friend

Send them `Install-TimestampHotkey.ps1`. They right-click → Run with PowerShell → done.

If their machine blocks unsigned scripts:
```powershell
Unblock-File .\Install-TimestampHotkey.ps1
```

---

*Packaged by Antigravity · 2026-07-01*
