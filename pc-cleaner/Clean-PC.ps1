# Self-elevate to Administrator if not already elevated
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Requesting Administrator privileges to clean system services..." -ForegroundColor Yellow
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        PC ESSENTIALS CLEANUP & FRESH UP  " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Running with Administrator privileges." -ForegroundColor Gray
Write-Host ""

# 1. Terminate orphaned Excel and Outlook processes
Write-Host "[1/4] Checking for orphaned Office processes..." -ForegroundColor Cyan
$excelProcesses = Get-CimInstance Win32_Process -Filter "Name = 'excel.exe'"
foreach ($proc in $excelProcesses) {
    if ($proc.CommandLine -like "*Embedding*") {
        Write-Host "  -> Found orphaned background Excel process (PID: $($proc.ProcessId)). Killing it..." -ForegroundColor Yellow
        Stop-Process -Id $proc.ProcessId -Force
    }
}

$outlookProcesses = Get-CimInstance Win32_Process -Filter "Name = 'outlook.exe'"
foreach ($proc in $outlookProcesses) {
    $p = Get-Process -Id $proc.ProcessId -ErrorAction SilentlyContinue
    if ($p -and $p.MainWindowHandle -eq 0) {
        Write-Host "  -> Found orphaned background Outlook process (PID: $($proc.ProcessId)). Killing it..." -ForegroundColor Yellow
        Stop-Process -Id $proc.ProcessId -Force
    }
}
Write-Host "  Office processes checked." -ForegroundColor Green

# 2. Terminate stuck UWP/System services and apps (CPU > 50%)
Write-Host "[2/4] Checking for stuck UWP services and background apps..." -ForegroundColor Cyan
$monitoredServices = @("StateRepository", "camsvc", "CrossDeviceService")
foreach ($serviceName in $monitoredServices) {
    $svc = Get-CimInstance Win32_Service -Filter "Name = '$serviceName'"
    if ($svc -and $svc.State -eq "Running" -and $svc.ProcessId -gt 0) {
        $perf = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.IDProcess -eq $svc.ProcessId }
        if ($perf -and $perf.PercentProcessorTime -gt 50) {
            Write-Host "  -> Service '$serviceName' (PID: $($svc.ProcessId)) is consuming excessive CPU ($($perf.PercentProcessorTime)%). Killing svchost to restart it..." -ForegroundColor Red
            Stop-Process -Id $svc.ProcessId -Force
        }
    }
}

$uwpApps = @("PhoneExperienceHost", "YourPhoneAppProxy", "SearchFilterHost", "SearchProtocolHost")
foreach ($appName in $uwpApps) {
    $procs = Get-Process -Name $appName -ErrorAction SilentlyContinue
    foreach ($p in $procs) {
        $perf = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.IDProcess -eq $p.Id }
        if ($perf -and $perf.PercentProcessorTime -gt 50) {
            Write-Host "  -> App '$appName' (PID: $($p.Id)) is consuming excessive CPU ($($perf.PercentProcessorTime)%). Terminating it..." -ForegroundColor Red
            Stop-Process -Id $p.Id -Force
        }
    }
}
Write-Host "  Stuck UWP/System services checked." -ForegroundColor Green

# 3. Network & DNS Flush
Write-Host "[3/4] Flushing DNS cache..." -ForegroundColor Cyan
Clear-DnsClientCache
Write-Host "  DNS cache successfully flushed." -ForegroundColor Green

# 4. Safe Temporary Files Cleanup
Write-Host "[4/4] Cleaning temporary folders..." -ForegroundColor Cyan
$tempFolders = @($env:TEMP, "C:\Windows\Temp")
$deletedCount = 0
$failedCount = 0
foreach ($folder in $tempFolders) {
    if (Test-Path $folder) {
        $items = Get-ChildItem -Path $folder -File -Recurse -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            try {
                Remove-Item $item.FullName -Force -ErrorAction Stop
                $deletedCount++
            } catch {
                $failedCount++
            }
        }
    }
}
Write-Host "  Temp cleanup finished: $deletedCount files deleted ($failedCount locked files skipped)." -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        CLEANUP COMPLETE! SYSTEM FRESHENED " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
