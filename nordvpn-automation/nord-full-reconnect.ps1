# nord-full-reconnect.ps1
# Performs a full NordVPN disconnect + reconnect via Windows UI Automation.
# Required when NordVPN Threat Protection was toggled and Chrome DNS is still broken.
# The 'Reconnect' button does a soft reconnect that does NOT flush the WFP driver state.
# This script does the real sequence: Pause -> Disconnect (confirm dialog) -> Quick Connect.
#
# Usage: powershell -ExecutionPolicy Bypass -File nord-full-reconnect.ps1
# Tested on NordVPN app version 8.6.2.0 (Windows)

Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Windows.Forms

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class NordReconnectWin32 {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, int x, int y, uint d, int e);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    public static void Click(int x, int y) {
        SetCursorPos(x, y); System.Threading.Thread.Sleep(120);
        mouse_event(0x0002, x, y, 0, 0); System.Threading.Thread.Sleep(80);
        mouse_event(0x0004, x, y, 0, 0);
    }
}
'@

$proc = Get-Process NordVPN -EA SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
if (-not $proc) { Write-Host 'NordVPN not running'; exit }

$root = [System.Windows.Automation.AutomationElement]::RootElement
$pc   = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ProcessIdProperty, $proc.Id)
$nw   = $root.FindFirst([System.Windows.Automation.TreeScope]::Children, $pc)

[NordReconnectWin32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 400

# 1. Navigate to VPN tab
$vpnCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, 'DashboardContainerViewModel')
$vpnTab  = $nw.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $vpnCond)
if ($vpnTab) {
    try { $vpnTab.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern).Select() }
    catch { $r=$vpnTab.Current.BoundingRectangle; [NordReconnectWin32]::Click([int]($r.X+$r.Width/2),[int]($r.Y+$r.Height/2)) }
    Start-Sleep -Milliseconds 600
    Write-Host 'On VPN tab'
}

# 2. Click Pause button to open Pause/Disconnect menu
$pauseCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, 'DashboardVpnPause')
$pauseBtn  = $nw.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $pauseCond)
if (-not $pauseBtn) { Write-Host 'Not connected (Pause button not found)'; exit }

$r = $pauseBtn.Current.BoundingRectangle
Write-Host 'Clicking Pause to open disconnect menu...'
[NordReconnectWin32]::Click([int]($r.X+$r.Width/2), [int]($r.Y+$r.Height/2))
Start-Sleep -Milliseconds 800

# 3. Click 'Disconnect' from the dropdown
$discCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, 'PauseDisconnect_Option')
$discEl   = $nw.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $discCond)
if ($discEl) {
    $r = $discEl.Current.BoundingRectangle
    [NordReconnectWin32]::Click([int]($r.X+$r.Width/2), [int]($r.Y+$r.Height/2))
    Write-Host 'Clicked Disconnect'
    Start-Sleep -Milliseconds 800
}

# 4. Confirm the 'Pause auto-connect' dialog if it appears
$primaryCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, 'PrimaryButton')
$primaryBtn  = $nw.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $primaryCond)
if ($primaryBtn) {
    $r = $primaryBtn.Current.BoundingRectangle
    [NordReconnectWin32]::Click([int]($r.X+$r.Width/2), [int]($r.Y+$r.Height/2))
    Write-Host 'Confirmed disconnect dialog'
}

Write-Host 'Waiting 5s for VPN to fully drop...'
Start-Sleep -Seconds 5

# 5. Click Quick Connect to reconnect fresh
$qcCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, 'DashboardVpnQuickConnect')
$qcBtn  = $nw.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $qcCond)
if ($qcBtn) {
    $r = $qcBtn.Current.BoundingRectangle
    [NordReconnectWin32]::Click([int]($r.X+$r.Width/2), [int]($r.Y+$r.Height/2))
    Write-Host 'Reconnecting... waiting 10s'
    Start-Sleep -Seconds 10
}

# 6. Flush DNS and verify
ipconfig /flushdns | Out-Null
$dns = Resolve-DnsName www.google.com -Type A -EA SilentlyContinue
Write-Host "DNS result: $($dns.IPAddress -join ', ')"
if ($dns.IPAddress -notcontains '192.0.0.88') {
    Write-Host 'SUCCESS - VPN reconnected with clean DNS'
} else {
    Write-Host 'Still 192.0.0.88 - check that Threat Protection is OFF in NordVPN'
}
