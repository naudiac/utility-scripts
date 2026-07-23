<#
.SYNOPSIS
    Automated optimization script for Samsung Galaxy Watch (Wear OS / One UI Watch).
.DESCRIPTION
    Applies UI responsiveness tweaks (0.0x animations), disables background voice listening
    (Bixby & Assistant wakeup), disables unused payment apps, and removes store demo/diagnostic bloatware.
.PARAMETER DeviceAddress
    Optional IP:Port address of the watch (e.g., 192.168.4.122:45867 or IP for auto-connect).
.EXAMPLE
    .\Optimize-GalaxyWatch.ps1
.EXAMPLE
    .\Optimize-GalaxyWatch.ps1 -DeviceAddress "192.168.4.122:45867"
#>

[CmdletBinding()]
param(
    [string]$DeviceAddress = ""
)

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   Samsung Galaxy Watch (Wear OS) ADB Optimizer      " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Ensure ADB is available
if (-not (Get-Command "adb" -ErrorAction SilentlyContinue)) {
    Write-Error "ADB CLI not found in PATH. Please install Android Platform Tools."
    exit 1
}

# Connect if DeviceAddress specified
if ($DeviceAddress) {
    Write-Host "[*] Connecting to $DeviceAddress..." -ForegroundColor Yellow
    adb connect $DeviceAddress
}

# Check ADB connection status
$devices = adb devices
if ($devices -notmatch "\tdevice") {
    Write-Error "No ADB device connected. Please pair/connect your Galaxy Watch first via 'adb pair' and 'adb connect'."
    exit 1
}

$model = (adb shell getprop ro.product.model).Trim()
$build = (adb shell getprop ro.build.display.id).Trim()
Write-Host "[+] Connected Watch Model: $model ($build)" -ForegroundColor Green
Write-Host ""

# 1. UI Animation Scales (Instant Responsiveness)
Write-Host "[1/4] Setting UI animation scales to 0.0x (Instant transitions)..." -ForegroundColor Yellow
adb shell "settings put global window_animation_scale 0.0"
adb shell "settings put global transition_animation_scale 0.0"
adb shell "settings put global animator_duration_scale 0.0"
Write-Host "  -> Animation scales updated to 0.0." -ForegroundColor Green

# 2. Disable Background Voice Assistant Wakeups
Write-Host "[2/4] Disabling background voice assistant wakeups..." -ForegroundColor Yellow
$voicePackages = @(
    "com.samsung.android.bixby.wakeup",
    "com.google.android.wearable.assistant"
)
foreach ($pkg in $voicePackages) {
    adb shell "pm disable-user --user 0 $pkg" | Out-Null
    Write-Host "  -> Disabled: $pkg" -ForegroundColor Green
}

# 3. Disable Contactless Payment Apps
Write-Host "[3/4] Disabling watch payment services..." -ForegroundColor Yellow
$payPackages = @(
    "com.samsung.android.samsungpay.gear",
    "com.google.android.apps.walletnfcrel"
)
foreach ($pkg in $payPackages) {
    adb shell "pm disable-user --user 0 $pkg" | Out-Null
    Write-Host "  -> Disabled: $pkg" -ForegroundColor Green
}

# 4. Disable System Bloatware & Diagnostic Tracking
Write-Host "[4/4] Disabling system bloatware & background diagnostic tracking..." -ForegroundColor Yellow
$bloatPackages = @(
    "com.samsung.android.dqagent",
    "com.google.android.apps.wearable.retailattractloop",
    "com.samsung.android.wearable.setupwizard.fota"
)
foreach ($pkg in $bloatPackages) {
    adb shell "pm disable-user --user 0 $pkg" | Out-Null
    Write-Host "  -> Disabled: $pkg" -ForegroundColor Green
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   Optimization Complete! Watch is ready and snappy.  " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
