---
name: google-drive-upload
description: >
  Upload files to William's Google Drive using the taylorwilsdon_workspace
  MCP server. Trigger when the user says anything like "save to my gdrive",
  "upload to google drive", "put this in my drive", "back this up to gdrive",
  "save in gdrive", or similar. Uses create_drive_file or update_drive_file
  MCP tools — no Python scripts needed.
---

# Google Drive Upload Skill

## Overview

Drive uploads are handled via the **`taylorwilsdon_workspace` MCP server**.
Use `create_drive_file` for new files and `update_drive_file` for existing ones.
Always pass `user_google_email: naudiac@gmail.com`.

> [!NOTE]
> The old Python toolkit at `~\scratch\Google_Drive_Tools_Kit\` is retired.
> Use the MCP tools below for all uploads.

## How To Upload

### New file into a specific folder
```
create_drive_file(
  file_name="filename.ext",
  content="...",
  folder_id="FOLDER_ID",
  user_google_email="naudiac@gmail.com"
)
```

### Update an existing file
```
update_drive_file(
  file_id="FILE_ID",
  content="...",
  user_google_email="naudiac@gmail.com"
)
```

### Find a folder ID first (if unsure)
```
search_drive_files(query="name = 'Folder Name'", user_google_email="naudiac@gmail.com")
```

## William's Drive Structure (Key Folder IDs)

| Folder | ID |
|---|---|
| **Gemini Experiments** *(default for AI tools/scripts)* | `1o1mn51Vrgm1esCCrizaphG7GCElJk91C` |
| _Agent_Skills & Toolkits | `1MFSnh6nzlyNALcNn80RKUnOBW7hc_JYJ` |
| Assets & Archives | `1ubH_4V6GYsn-vKPeWdIMYmD9fhzprgtc` |
| Prompts & Blueprints | `1UUcypKzPWG_xpE0Q71ALduWPurXB6YKt` |
| Automation Vault | `1-yyV-8WgG4uGgweXv_BRiCUwtm5VY953` |
| Business Plans | `15r499_HYaRFI5bvOhOY9FKPOuNOAcPXa` |
| Business Ideas | `1D1jser48PZ6DjifXEUVp_KkxBiGjLkQ1` |
| Project Folder | `1bskG3tQiRKXARbgLJbukOBYAVyvBb7J2` |
| MISC | `1r-vebw3zoxS9k3iimQmO4to70VF39e-Z` |
| ARCHIVES | `1dT_TIXhrqKqCDTPEWVPvspbcmU4PFODf` |
| BIZ | `14X3B5LP7o_zZYOdCwY_pfRa7uwZVMuHy` |
| Paystubs (Send to Kim) | `1bjbJJ6KJbuZ3AlOsTM2B3qOztA-zzYMs` |

> **Default upload target for AI-generated tools/scripts:** `Gemini Experiments → _Agent_Skills & Toolkits`

## Authentication

Handled automatically by `taylorwilsdon_workspace`. Credentials stored at:
`C:\Users\whanusiewicz\.google_workspace_mcp\credentials\naudiac@gmail.com.json`

If token expires, see the re-auth steps in the `google-workspace-ops` skill.
