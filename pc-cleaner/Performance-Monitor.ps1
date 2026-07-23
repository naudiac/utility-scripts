# PowerShell Performance Monitor & Report Generator

# Paths
$BaseDir = "C:\Users\whanusiewicz\.gemini\antigravity\scratch\utility-scripts"
$ReviewDir = Join-Path $BaseDir "knowledge_base\performance_reviews"
$HistoryFile = Join-Path $BaseDir "pc-cleaner\perf_history.json"

# Create directories if they do not exist
if (-not (Test-Path $ReviewDir)) {
    New-Item -ItemType Directory -Path $ReviewDir -Force | Out-Null
}

# 1. Gather System Metrics
# Overall CPU Usage
$CpuQuery = Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name = '_Total'"
$CpuLoad = if ($CpuQuery) { $CpuQuery.PercentProcessorTime } else { 0 }

# Memory Stats
$Os = Get-CimInstance Win32_OperatingSystem
$TotalRam = [math]::Round($Os.TotalVisibleMemorySize / 1MB, 2)
$FreeRam = [math]::Round($Os.FreePhysicalMemory / 1MB, 2)
$UsedRam = [math]::Round($TotalRam - $FreeRam, 2)
$RamPercent = [math]::Round(($UsedRam / $TotalRam) * 100, 2)

# Top 5 CPU Processes
$CpuProcesses = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | 
    Where-Object { $_.Name -ne '_Total' -and $_.Name -ne 'Idle' } | 
    Sort-Object PercentProcessorTime -Descending | 
    Select-Object -First 5 | 
    ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            PID  = $_.IDProcess
            CPU  = $_.PercentProcessorTime
        }
    }

# Top 5 Memory Processes (Working Set)
$MemProcesses = Get-Process | 
    Sort-Object WorkingSet -Descending | 
    Select-Object -First 5 | 
    ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            PID  = $_.Id
            RAM  = [math]::Round($_.WorkingSet / 1MB, 2)
        }
    }

# Scan for anomalies (stuck services/orphans)
$Anomalies = @()

# Checking for background orphaned Excel processes
$excelProcesses = Get-CimInstance Win32_Process -Filter "Name = 'excel.exe'"
foreach ($proc in $excelProcesses) {
    if ($proc.CommandLine -like "*Embedding*") {
        $Anomalies += "Orphaned background Excel process found (PID $($proc.ProcessId))."
    }
}

# Checking for stuck system services
$monitoredServices = @("StateRepository", "camsvc", "CrossDeviceService")
foreach ($serviceName in $monitoredServices) {
    $svc = Get-CimInstance Win32_Service -Filter "Name = '$serviceName'"
    if ($svc -and $svc.State -eq "Running" -and $svc.ProcessId -gt 0) {
        $perf = Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.IDProcess -eq $svc.ProcessId }
        if ($perf -and $perf.PercentProcessorTime -gt 50) {
            $Anomalies += "Service '$serviceName' is spinning at $($perf.PercentProcessorTime)% CPU (PID $($svc.ProcessId))."
        }
    }
}

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 2. Update Performance History Database
$Entry = [PSCustomObject]@{
    Timestamp = $Timestamp
    CPU       = $CpuLoad
    RAM_Total = $TotalRam
    RAM_Used  = $UsedRam
    RAM_Free  = $FreeRam
    RAM_Pct   = $RamPercent
    Anomalies = $Anomalies
}

$History = @()
if (Test-Path $HistoryFile) {
    try {
        $History = Get-Content $HistoryFile -Raw | ConvertFrom-Json
        if ($History -isnot [System.Array]) {
            $History = @($History)
        }
    } catch {
        $History = @()
    }
}

$History += $Entry
# Keep last 100 history logs
if ($History.Count -gt 100) {
    $History = $History[-100..-1]
}

$History | ConvertTo-Json -Depth 4 | Out-File $HistoryFile -Encoding utf8

# 3. Generate Daily Report
$DailyPath = Join-Path $ReviewDir "daily_report.md"
$DailyMD = @"
# PC Daily Performance Review
**Last Checked:** $Timestamp

## System Load Summary
*   **Average CPU Load:** $CpuLoad %
*   **RAM Status:** $UsedRam GB used / $TotalRam GB total ($RamPercent % utilized)
*   **Free RAM Available:** $FreeRam GB

## Potential Issues & Anomalies
$(
if ($Anomalies.Count -eq 0) {
    "No performance anomalies or orphaned background processes detected. Your system is running clean!"
} else {
    $anomList = ""
    foreach ($anom in $Anomalies) {
         $anomList += "*   [WARNING] $anom`n"
    }
    $anomList + "`n*Tip: Run the 'Fresh Up' script on your desktop to instantly clean these processes.*"
}
)

## Resource Consumers

### Top 5 CPU Consumers
| Process Name | PID | CPU Usage (%) |
| :--- | :--- | :--- |
$(
$cpuRows = ""
foreach ($p in $CpuProcesses) {
    $cpuRows += "| $($p.Name) | $($p.PID) | $($p.CPU)% |`n"
}
$cpuRows
)

### Top 5 Memory Consumers
| Process Name | PID | RAM Usage (MB) |
| :--- | :--- | :--- |
$(
$memRows = ""
foreach ($p in $MemProcesses) {
    $memRows += "| $($p.Name) | $($p.PID) | $($p.RAM) MB |`n"
}
$memRows
)
"@

$DailyMD | Out-File $DailyPath -Encoding utf8

# 4. Generate Weekly Report
# Aggregates average stats from all entries in the last 7 days
$SevenDaysAgo = (Get-Date).AddDays(-7)
$WeeklyEntries = $History | Where-Object { 
    [datetime]$_.Timestamp -ge $SevenDaysAgo 
}

if ($WeeklyEntries.Count -eq 0) {
    $WeeklyEntries = @($Entry)
}

$AvgWeeklyCpu = [math]::Round(($WeeklyEntries | Measure-Object -Property CPU -Average).Average, 2)
$AvgWeeklyRam = [math]::Round(($WeeklyEntries | Measure-Object -Property RAM_Pct -Average).Average, 2)
$TotalAnomalies = ($WeeklyEntries | Where-Object { $_.Anomalies -and $_.Anomalies.Count -gt 0 }).Count

$WeeklyPath = Join-Path $ReviewDir "weekly_report.md"
$WeeklyMD = @"
# PC Weekly Performance Review
**Period:** $($SevenDaysAgo.ToString("yyyy-MM-dd")) to $((Get-Date).ToString("yyyy-MM-dd"))

## Weekly Trend Averages
*   **Weekly Avg CPU Load:** $AvgWeeklyCpu %
*   **Weekly Avg RAM Utilization:** $AvgWeeklyRam %
*   **Total Days with Performance Flags:** $TotalAnomalies day(s) out of $($WeeklyEntries.Count) checks

## Performance Insights
*   **RAM Capacity:** Your 32GB system continues to have comfortable headroom. Keep active tabs and background tools managed to maintain high speed.
*   **Anomalies:** If you experience regular slowness, review the Daily reports to verify if specific system services like `StateRepository` or `camsvc` are looping.

## History Logs (Last 7 Days)
| Timestamp | Avg CPU Load | RAM Utilized (%) | Flags Raised |
| :--- | :--- | :--- | :--- |
$(
$histRows = ""
foreach ($e in $WeeklyEntries) {
    $flagCount = if ($e.Anomalies) { $e.Anomalies.Count } else { 0 }
    $histRows += "| $($e.Timestamp) | $($e.CPU)% | $($e.RAM_Pct)% | $flagCount |`n"
}
$histRows
)
"@

$WeeklyMD | Out-File $WeeklyPath -Encoding utf8

Write-Host "Performance reports generated successfully!" -ForegroundColor Green
