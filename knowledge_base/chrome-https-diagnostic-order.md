# Chrome HTTPS Diagnostic Order

When Chrome shows HTTPS errors (`ERR_QUIC_PROTOCOL_ERROR`, `ERR_CONNECTION_CLOSED`, `ERR_SSL_*`) but `Invoke-WebRequest https://...` in PowerShell succeeds, the cause is **NEVER Chrome itself first**. Always diagnose in this order — DO NOT reinstall Chrome before completing these steps:

## Step 1 — Check DNS (30 seconds)
```powershell
Resolve-DnsName www.google.com -Type A
```
Real Google IPs start with: `142.250.x`, `172.217.x`, `74.125.x`, `216.58.x`
If you see anything else (e.g. `192.0.0.88`) → DNS is being intercepted.

## Step 2 — Identify who is intercepting DNS
```powershell
Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses }
Get-Process | Where-Object { $_.Name -like "*nord*" -or $_.Name -like "*vpn*" -or $_.Name -like "*threat*" }
```

## Step 3 — NordVPN Threat Protection (confirmed sole cause on this machine)
- Service name: `nordsec-threatprotection-service`
- Symptom: DNS returns `192.0.0.88` instead of real IPs; Chrome QUIC and TLS both fail; PowerShell works
- **Root cause confirmed (2026-07-10):** Threat Protection ON causes WFP driver to blackhole all DNS to `192.0.0.88`. Toggling TP OFF in the UI is NOT enough — the WFP driver state lags. A full VPN disconnect + reconnect is required to flush it.
- **Fix (exact sequence):**
  1. NordVPN app → Shield icon (2nd icon in left sidebar) → Threat Protection → **OFF**
  2. On the main VPN screen, click **Pause** → select **Disconnect** from the menu → confirm the dialog
  3. Wait ~5 seconds for NordLynx adapter to go down
  4. Click **Secure my connection** (Quick Connect) to reconnect fresh
  5. Flush DNS: `ipconfig /flushdns`
  6. Chrome should now work normally — no restart needed
- **Note:** Stopping `nordsec-threatprotection-service` via PowerShell does NOT work — the service auto-restarts and the WFP driver continues filtering at kernel level. The only reliable fix is a full disconnect+reconnect from within the NordVPN UI.
- **NordVPN custom DNS setting does NOT work** — even setting 1.1.1.1 in Connection and Security → Custom DNS and doing a full reconnect, the NordLynx adapter still gets hardcoded to `103.86.96.100`. Do not waste time on this path.
- **⚠️ Also do Step 4 alongside this fix** — NordVPN's Chrome extension force-install policy creates a second browser-level proxy layer that keeps Chrome broken even after the OS DNS is fixed. Remove the extension key (Step 4) as part of the same fix, not as a fallback.

## Step 4 — Chrome shows "Managed by your organization"
- This is caused by NordVPN force-installing its Chrome extension via a registry policy key.
- The key is at: `HKLM:\SOFTWARE\Policies\Google\Chrome\ExtensionInstallForcelist`
- It does NOT mean corporate control — it's just Nord's extension auto-install mechanism.
- A second policy key at `LocalNetworkAccessAllowedForUrls` is from WIT Logistics (SharePoint access) — leave that one alone.
- The "managed" label will persist as long as any policy key exists under `HKLM:\SOFTWARE\Policies\Google\Chrome`.
- The "Use secure DNS" (DoH) toggle in Chrome is grayed out on managed browsers — this is the side effect.
- To remove Nord's policy key (run as admin): `Remove-Item 'HKLM:\SOFTWARE\Policies\Google\Chrome\ExtensionInstallForcelist' -Force`

## Step 5 — Clear Zombie/Deadlocked Background Processes
- **Symptom:** Even after resolving the DNS and registry keys (Steps 1–4), attempting to launch Chrome (visibly or via Scheduled Task) results in a complete hang. The UI never appears, but a `chrome.exe` process sits in the background.
- **Cause:** When the kernel driver blackholed all the DNS traffic earlier, existing background browser processes (which handle extensions, WebView2, or pre-caching) crashed or deadlocked. These "zombies" prevent any new visible instances from spawning.
- **Fix:**
  1. Forcefully kill all Chrome processes: `taskkill /F /IM chrome.exe /T`
  2. Forcefully kill all Edge processes (as they share WebView2 layers): `taskkill /F /IM msedge.exe /T`
  3. Re-launch the browser directly via the Windows Shell (e.g. `start "" "https://google.com"`).

## Step 6 — Only if Steps 1–5 clear and Chrome still fails
THEN investigate Chrome flags (`chrome://flags`), profile corruption, SSL state files, or reinstall.

## Diagnostics & Verification Strategy
When diagnosing browser UI or network issues (like the NordVPN crash), you are operating blind from a background session. You **MUST** persist and use the `desktop-screenshot` skill repeatedly after every single action to visually confirm whether windows have appeared, hung, or thrown errors on the user's screen. Never assume a GUI command succeeded just because the terminal exited with code 0.
