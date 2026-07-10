# NordVPN UI Automation Scripts

PowerShell scripts for controlling NordVPN via Windows UI Automation (UIA).
Built during a 2026-07-10 debugging session to resolve Chrome DNS blackholing caused by NordVPN Threat Protection.

## Background

When NordVPN's **Threat Protection** is ON, the WFP (Windows Filtering Platform) kernel driver redirects all DNS queries to `192.0.0.88` (Nord's blackhole), causing Chrome to fail with `ERR_QUIC_PROTOCOL_ERROR`. Toggling TP off in the UI is not enough — the WFP driver state lags and requires a **full disconnect + reconnect** to flush.

## Scripts

### `nord-full-reconnect.ps1`
Performs a full NordVPN disconnect → reconnect via UI Automation.

**When to use:** After toggling Threat Protection OFF and Chrome DNS is still broken (`192.0.0.88`).

**What it does:**
1. Navigates to the VPN tab
2. Clicks Pause → Disconnect from the dropdown menu
3. Confirms the auto-connect pause dialog
4. Waits for NordLynx to drop
5. Clicks Quick Connect to reconnect fresh
6. Flushes DNS and verifies resolution

```powershell
powershell -ExecutionPolicy Bypass -File nord-full-reconnect.ps1
```

## Key AutomationIds (NordVPN 8.6.2.0)

| Element | AutomationId |
|---|---|
| VPN tab | `DashboardContainerViewModel` |
| Pause/Disconnect button | `DashboardVpnPause` |
| Disconnect menu option | `PauseDisconnect_Option` |
| Confirm dialog primary button | `PrimaryButton` |
| Quick Connect button | `DashboardVpnQuickConnect` |
| Connection options dropdown | `DashboardVpnConnectionOptions` |
| TP menu item | `ThreatProtectionMenuItem` |
| Custom DNS section | `SettingsViewCustomDnsSection` |
| Custom DNS toggle | `SettingsViewUseCustomDnsSwitch` |
| DNS expander chevron | `ExpanderChevronArea` |
| DNS input boxes | `DnsHostTextBox` |

## Known Limitations

- **Custom DNS UI setting does not work** — even after setting `1.1.1.1` and doing a full reconnect, the NordLynx adapter is hardcoded to `103.86.96.100` (Nord's servers). The UI setting is cosmetic.
- **`Set-DnsClientServerAddress` requires admin elevation** to override the NordLynx adapter DNS directly.
- **Chrome extension conflict** — NordVPN force-installs a Chrome extension via `HKLM:\SOFTWARE\Policies\Google\Chrome\ExtensionInstallForcelist`. This creates a second browser-level proxy layer. Remove it (as admin) to prevent double-routing: `Remove-Item 'HKLM:\SOFTWARE\Policies\Google\Chrome\ExtensionInstallForcelist' -Force`
