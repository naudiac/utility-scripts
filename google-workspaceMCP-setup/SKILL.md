---
name: google-workspaceMCP-setup
description: >-
  Installs and configures the taylorwilsdon_workspace MCP server (workspace-mcp)
  on a Windows machine for Gmail and Google Drive access via Antigravity.
  Covers fresh installation, first-time OAuth, and re-authentication when tokens
  expire. Use when setting up a new machine or when the server fails to start
  with auth errors.
---

# Google Workspace MCP — Setup & Re-Authentication

## Overview

The `taylorwilsdon_workspace` MCP server (workspace-mcp v1.22.0) provides
Gmail and Drive tools natively inside Antigravity. This skill covers:

- **Fresh install** on a new Windows machine
- **Re-authentication** when the OAuth token expires or is revoked
- **Colleague machine** notes where setup differs

> [!IMPORTANT]
> This is a **Windows-specific** skill. The binary paths, credential locations,
> and PowerShell commands assume Windows. For a colleague's machine, see the
> "Colleague Machine Notes" section.

---

## Prerequisites

- **uv** must be installed. Run `uv --version` to check. If missing, install:
  ```powershell
  winget install astral-sh.uv
  # or
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Google OAuth client credentials (the Client ID + Secret). These are stored
  in `mcp_config.json` and the `google-workspace-ops` skill reference.

---

## Fresh Installation

### Step 1 — Install workspace-mcp

```powershell
uv tool install --system-certs workspace-mcp
```

This installs ~93 packages and places two binaries in `%USERPROFILE%\.local\bin\`:
- `workspace-mcp.exe` — the MCP server
- `workspace-cli.exe` — CLI tool for triggering auth

> [!NOTE]
> The `--system-certs` flag is required on corporate/proxy networks (TLS
> interception). It tells uv to use the Windows certificate store.

### Step 2 — Add to MCP config

Edit `C:\Users\whanusiewicz\.gemini\config\mcp_config.json` and add inside
`"mcpServers"`:

```json
"taylorwilsdon_workspace": {
  "command": "C:\\Users\\whanusiewicz\\.local\\bin\\workspace-mcp.exe",
  "args": [
    "--tools",
    "gmail",
    "drive",
    "--single-user"
  ],
  "env": {
    "GOOGLE_OAUTH_CLIENT_ID": "<YOUR_CLIENT_ID>",
    "GOOGLE_OAUTH_CLIENT_SECRET": "<YOUR_CLIENT_SECRET>",
    "GOOGLE_WORKSPACE_USER": "naudiac@gmail.com"
  }
}
```

> [!NOTE]
> The GitHub backup of the full `mcp_config.json` is at:
> `https://github.com/naudiac/antigravity-config` (private repo, `naudiac`)

### Step 3 — First-time OAuth

The server needs a one-time browser auth before it can start without blocking.

**3a.** Start the server temporarily in HTTP mode:
```powershell
$env:GOOGLE_OAUTH_CLIENT_ID="<YOUR_CLIENT_ID>"
$env:GOOGLE_OAUTH_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
C:\Users\whanusiewicz\.local\bin\workspace-mcp.exe --tools gmail drive --single-user --transport streamable-http
```

**3b.** In a second PowerShell window, trigger the auth flow:
```powershell
$env:GOOGLE_OAUTH_CLIENT_ID="<YOUR_CLIENT_ID>"
$env:GOOGLE_OAUTH_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
C:\Users\whanusiewicz\.local\bin\workspace-cli.exe call start_google_auth service_name=gmail user_google_email=naudiac@gmail.com
```

**3c.** Copy the long `Authorization URL` printed to the terminal and paste it
into your browser. Sign in as `naudiac@gmail.com` and click **Allow**.

**3d.** The browser will redirect to `localhost:8000/oauth2callback` and show
**"Authentication Successful"**. The server saves credentials to:
```
C:\Users\whanusiewicz\.google_workspace_mcp\credentials\naudiac@gmail.com.json
```

**3e.** Kill the HTTP server (`Ctrl+C` in the first window).

### Step 4 — Restart Antigravity

On next startup, the MCP server will initialize instantly using the saved
credentials. No browser interaction needed.

---

## Re-Authentication (Token Expired)

Token expiry symptoms: `taylorwilsdon_workspace` shows MCP Error, tools return
401/403, or auth-related errors in server logs.

Repeat **Step 3** above exactly — the OAuth flow is the same. The new token
will overwrite the old one at the same credentials path.

> [!TIP]
> Tokens typically last months. Expiry is rare unless the Google account
> password changes or access is explicitly revoked in Google Account settings.

---

## Colleague Machine Notes

If setting up on a colleague's Windows machine, the only differences are:

| Item | William's Machine | Colleague's Machine |
|---|---|---|
| Binary path in mcp_config | `C:\Users\whanusiewicz\.local\bin\workspace-mcp.exe` | `C:\Users\<their-username>\.local\bin\workspace-mcp.exe` |
| `GOOGLE_WORKSPACE_USER` env | `naudiac@gmail.com` | their Google account email |
| Credentials saved to | `~\.google_workspace_mcp\credentials\naudiac@gmail.com.json` | `~\.google_workspace_mcp\credentials\<their-email>.json` |

The OAuth Client ID and Secret are shared — same values.

---

## Verification

After setup, verify all tools work:
```
search_gmail_messages(query="in:inbox", user_google_email="naudiac@gmail.com")
list_drive_items(user_google_email="naudiac@gmail.com")
```

Both should return results without errors.

---

## Reference

| Item | Value |
|---|---|
| Binary | `C:\Users\whanusiewicz\.local\bin\workspace-mcp.exe` |
| CLI tool | `C:\Users\whanusiewicz\.local\bin\workspace-cli.exe` |
| Credentials | `C:\Users\whanusiewicz\.google_workspace_mcp\credentials\naudiac@gmail.com.json` |
| MCP config | `C:\Users\whanusiewicz\.gemini\config\mcp_config.json` |
| GitHub backup | `https://github.com/naudiac/antigravity-config` (private) |
| Drive backup | `Gemini Experiments → _Agent_Skills & Toolkits → mcp_config.json` |
| Package version | workspace-mcp v1.22.0 |
| OAuth Client ID | `<YOUR_CLIENT_ID>` |
