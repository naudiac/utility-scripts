<#
.SYNOPSIS
    Timestamp Hotkey -- Install / Uninstall
    Binds Ctrl+Alt+D globally to copy yyyy-MM-dd_HH-mm-ss to clipboard.
    Zero background processes. Purely a Start Menu .lnk + VBScript.

.USAGE
    Install:   Right-click -> "Run with PowerShell"
               (or: .\Install-TimestampHotkey.ps1 -Install)
    Uninstall: .\Install-TimestampHotkey.ps1 -Uninstall

.NOTES
    Author : William Hanusiewicz (packaged by Antigravity)
    Created: 2026-07-01
    Version: 1.0
#>

param(
    [switch]$Install,
    [switch]$Uninstall
)

# -- Paths --------------------------------------------------------------------
$ScriptsDir = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "Scripts"
$VbsPath    = Join-Path $ScriptsDir "SilentTime.vbs"
$StartMenu  = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$LnkPath    = Join-Path $StartMenu "SilentTime.lnk"
$Hotkey     = "Ctrl+Alt+D"

# -- Helpers ------------------------------------------------------------------
function Write-Header {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "   Timestamp Hotkey  ($Hotkey)        " -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Installed {
    return (Test-Path $LnkPath) -and (Test-Path $VbsPath)
}

# -- Install ------------------------------------------------------------------
function Invoke-Install {
    Write-Host "[INSTALL] Creating Scripts folder..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $ScriptsDir | Out-Null

    Write-Host "[INSTALL] Writing SilentTime.vbs..." -ForegroundColor Yellow
    Set-Content -Path $VbsPath -Value `
        'CreateObject("WScript.Shell").Run "powershell.exe -NoProfile -Command ""Set-Clipboard (Get-Date -Format ''yyyy-MM-dd_HH-mm-ss'')""", 0, False'

    Write-Host "[INSTALL] Creating Start Menu shortcut with $Hotkey..." -ForegroundColor Yellow
    $shell                     = New-Object -ComObject WScript.Shell
    $shortcut                  = $shell.CreateShortcut($LnkPath)
    $shortcut.TargetPath       = "$env:SystemRoot\System32\wscript.exe"
    $shortcut.Arguments        = "`"$VbsPath`""
    $shortcut.WorkingDirectory = $ScriptsDir
    $shortcut.Description      = "Copy timestamp yyyy-MM-dd_HH-mm-ss to clipboard"
    $shortcut.WindowStyle      = 7
    $shortcut.Hotkey           = $Hotkey
    $shortcut.Save()

    Write-Host ""
    Write-Host "[OK] Installed successfully!" -ForegroundColor Green
    Write-Host "     VBScript : $VbsPath" -ForegroundColor Gray
    Write-Host "     Shortcut : $LnkPath" -ForegroundColor Gray
    Write-Host "     Hotkey   : $Hotkey -> clipboard timestamp" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[NOTE] If hotkey does not fire immediately, sign out" -ForegroundColor DarkYellow
    Write-Host "       and back in once. Explorer re-reads .lnk hotkeys at login." -ForegroundColor DarkYellow
}

# -- Uninstall ----------------------------------------------------------------
function Invoke-Uninstall {
    $removed = $false

    if (Test-Path $LnkPath) {
        Remove-Item $LnkPath -Force
        Write-Host "[OK] Removed shortcut : $LnkPath" -ForegroundColor Green
        $removed = $true
    } else {
        Write-Host "[--] Shortcut not found (already removed?): $LnkPath" -ForegroundColor DarkGray
    }

    if (Test-Path $VbsPath) {
        Remove-Item $VbsPath -Force
        Write-Host "[OK] Removed VBScript : $VbsPath" -ForegroundColor Green
        $removed = $true
    } else {
        Write-Host "[--] VBScript not found (already removed?): $VbsPath" -ForegroundColor DarkGray
    }

    if ($removed) {
        Write-Host ""
        Write-Host "[OK] Uninstalled. The $Hotkey hotkey is now free." -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[--] Nothing to uninstall -- already clean." -ForegroundColor DarkYellow
    }
}

# -- Interactive menu (no flags passed) --------------------------------------
function Show-Menu {
    $installed = Test-Installed
    if ($installed) {
        $status = "INSTALLED"
        $color  = "Green"
    } else {
        $status = "NOT INSTALLED"
        $color  = "DarkYellow"
    }

    Write-Host "  Status : $status" -ForegroundColor $color
    Write-Host "  Hotkey : $Hotkey"
    Write-Host ""
    Write-Host "  [1] Install"
    Write-Host "  [2] Uninstall"
    Write-Host "  [Q] Quit"
    Write-Host ""
    $choice = Read-Host "Choice"

    switch ($choice.ToUpper()) {
        "1"     { Invoke-Install   }
        "2"     { Invoke-Uninstall }
        "Q"     { return }
        default { Write-Host "Invalid choice." -ForegroundColor Red }
    }
}

# -- Entry point --------------------------------------------------------------
Write-Header

if ($Uninstall) {
    Invoke-Uninstall
} elseif ($Install) {
    Invoke-Install
} else {
    Show-Menu
}

Write-Host ""
if (-not $Install -and -not $Uninstall) { pause }
