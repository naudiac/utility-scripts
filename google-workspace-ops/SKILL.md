---
name: google-workspace-ops
description: >-
  General-purpose Google Drive, Gmail, and Sheets operations skill.
  Uses the taylorwilsdon_workspace MCP server (workspace-mcp v1.22.0),
  authenticated as naudiac@gmail.com. Credentials stored at
  ~/.google_workspace_mcp/credentials/naudiac@gmail.com.json.
  Trigger for any Drive folder/file ops, Gmail draft/send/search/label,
  or reading file content from Drive.
---

# Google Workspace Ops

## Overview

All Gmail and Drive operations are handled via the **`taylorwilsdon_workspace`
MCP server** (workspace-mcp v1.22.0), authenticated as `naudiac@gmail.com`.
This server is loaded globally at startup — no scripts, no token files, no Python
needed. Just call the MCP tools directly.

> [!IMPORTANT]
> The old `gws.py` script approach is **retired and broken**. Do not use it.
> Always use the MCP tools below.

**Credentials location:** `C:\Users\whanusiewicz\.google_workspace_mcp\credentials\naudiac@gmail.com.json`  
**Binary:** `C:\Users\whanusiewicz\.local\bin\workspace-mcp.exe`  
**MCP server name:** `taylorwilsdon_workspace`  
**Always pass:** `user_google_email: naudiac@gmail.com` in every tool call.

---

## Gmail Tools

| Tool | Key Args | Notes |
|---|---|---|
| `search_gmail_messages` | `query`, `user_google_email` | Gmail search syntax (e.g. `in:inbox is:unread`) |
| `get_gmail_message_content` | `message_id`, `user_google_email` | Full message body + headers |
| `get_gmail_messages_content_batch` | `message_ids[]`, `user_google_email` | Batch fetch multiple messages |
| `get_gmail_thread_content` | `thread_id`, `user_google_email` | Full thread |
| `draft_gmail_message` | `to`, `subject`, `body`, `user_google_email` | Creates a draft |
| `send_gmail_message` | `to`, `subject`, `body`, `user_google_email` | Sends immediately |
| `list_gmail_labels` | `user_google_email` | Returns all 77+ labels |
| `manage_gmail_label` | `user_google_email`, ... | Create/update labels |
| `modify_gmail_message_labels` | `message_id`, `user_google_email` | Apply/remove labels |

## Drive Tools

| Tool | Key Args | Notes |
|---|---|---|
| `search_drive_files` | `query`, `user_google_email` | Drive query syntax |
| `list_drive_items` | `folder_id`, `user_google_email` | List folder contents |
| `get_drive_file_content` | `file_id`, `user_google_email` | Read file text/content |
| `create_drive_file` | `file_name`, `content`, `folder_id`, `user_google_email` | Upload a new file |
| `update_drive_file` | `file_id`, `content`, `user_google_email` | Update existing file |
| `create_drive_folder` | `name`, `parent_folder_id`, `user_google_email` | Create folder |
| `get_drive_shareable_link` | `file_id`, `user_google_email` | Get shareable URL |

## Known Drive Folder IDs

| Folder | ID |
|---|---|
| Gemini Experiments | `1o1mn51Vrgm1esCCrizaphG7GCElJk91C` |
| _Agent_Skills & Toolkits | `1MFSnh6nzlyNALcNn80RKUnOBW7hc_JYJ` |
| Assets & Archives | `1ubH_4V6GYsn-vKPeWdIMYmD9fhzprgtc` |
| Prompts & Blueprints | `1UUcypKzPWG_xpE0Q71ALduWPurXB6YKt` |
| Automation Vault | `1-yyV-8WgG4uGgweXv_BRiCUwtm5VY953` |
| Project Folder | `1bskG3tQiRKXARbgLJbukOBYAVyvBb7J2` |
| Paystubs (Send to Kim) | `1bjbJJ6KJbuZ3AlOsTM2B3qOztA-zzYMs` |

## Known Contacts

| Name | Email |
|---|---|
| Kimberly Shahgholi (Ciampa) | `Kim@ciampaorganization.com` |

## Re-Authentication

If the token expires (rare — typically after months of inactivity or a revocation):

```powershell
# Run workspace-mcp in HTTP mode temporarily and trigger auth via workspace-cli
$env:GOOGLE_OAUTH_CLIENT_ID="<YOUR_CLIENT_ID>"
$env:GOOGLE_OAUTH_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
C:\Users\whanusiewicz\.local\bin\workspace-mcp.exe --tools gmail drive --single-user --transport streamable-http
# In a second terminal:
C:\Users\whanusiewicz\.local\bin\workspace-cli.exe call start_google_auth service_name=gmail user_google_email=naudiac@gmail.com
# Copy the URL printed, paste into browser, complete OAuth, then restart Antigravity
```

## Installation Reference

- **Binary:** installed via `uv tool install --system-certs workspace-mcp`
- **MCP config:** `C:\Users\whanusiewicz\.gemini\config\mcp_config.json`
- **GitHub backup:** `https://github.com/naudiac/antigravity-config` (private)
- **Drive backup:** `Gemini Experiments → _Agent_Skills & Toolkits → mcp_config.json`
