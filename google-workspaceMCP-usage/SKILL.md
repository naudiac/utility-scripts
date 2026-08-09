---
name: google-workspaceMCP-usage
description: >-
  Guides the agent on using the taylorwilsdon_workspace MCP server for Gmail
  and Google Drive operations. Provides opinionated step-by-step workflows for
  common tasks (summarize email, find and read files, draft/send messages,
  upload to Drive) plus a full tool reference. Trigger for any request involving
  Gmail or Google Drive on naudiac@gmail.com.
---

# Google Workspace MCP — Usage Guide

## Overview

All Gmail and Drive operations go through the `taylorwilsdon_workspace` MCP
server. Always pass `user_google_email: "naudiac@gmail.com"` in every call.

> [!IMPORTANT]
> Never use the old `gws.py` scripts or `Google_Drive_Tools_Kit` Python scripts.
> Those are retired and broken. Always use the MCP tools below.

---

## Common Workflows

### 📬 "Show me / summarize my unread emails"

1. `search_gmail_messages` — query: `is:unread`, get message IDs
2. `get_gmail_messages_content_batch` — pass the list of message IDs
3. Summarize subject + sender + key body content for the user
4. If user wants to act on one, proceed to Reply or Label workflow

```
search_gmail_messages(query="is:unread", user_google_email="naudiac@gmail.com")
get_gmail_messages_content_batch(message_ids=[...], user_google_email="naudiac@gmail.com")
```

---

### 📨 "Find emails from / about [topic]"

1. `search_gmail_messages` — use Gmail search syntax (see tips below)
2. `get_gmail_messages_content_batch` — fetch content for matches
3. Present results with From / Subject / Date / snippet

**Gmail search tips:**
- `from:kim@ciampaorganization.com` — by sender
- `subject:invoice` — by subject keyword
- `in:inbox is:unread` — unread inbox
- `after:2026/06/01 before:2026/06/30` — date range
- `has:attachment` — emails with files
- `label:Financial` — by label

---

### ✉️ "Draft / send an email"

**Draft (save, don't send):**
```
draft_gmail_message(
  to="recipient@example.com",
  subject="Subject here",
  body="Body text here",
  user_google_email="naudiac@gmail.com"
)
```

**Send immediately:**
```
send_gmail_message(
  to="recipient@example.com",
  subject="Subject here",
  body="Body text here",
  user_google_email="naudiac@gmail.com"
)
```

> [!TIP]
> Always draft first for important emails. Confirm with the user before sending.

---

### 🏷️ "Label / organize an email"

1. `list_gmail_labels` — get label IDs (77 labels exist)
2. `modify_gmail_message_labels` — apply label to message

```
list_gmail_labels(user_google_email="naudiac@gmail.com")
modify_gmail_message_labels(
  message_id="...",
  add_label_ids=["Label_75"],   # e.g. Financial/Receipts/2026
  user_google_email="naudiac@gmail.com"
)
```

**Key label IDs to know:**

| Label | ID |
|---|---|
| INBOX | `INBOX` |
| STARRED | `STARRED` |
| Financial/Receipts & Purchases/2026 | `Label_75` |
| Financial/Personal Taxes/2026 | `Label_62` |
| Professional/Logistics & Supply Chain | `Label_94` |
| Review/Unsorted | `Label_67` |
| Review/Keepers (Docs & Travel) | `Label_74` |

---

### 🔍 "Find a file in Drive"

1. `search_drive_files` — use Drive query syntax
2. If found, optionally `get_drive_file_content` to read it

```
search_drive_files(query="name contains 'invoice'", user_google_email="naudiac@gmail.com")
get_drive_file_content(file_id="...", user_google_email="naudiac@gmail.com")
```

**Drive query tips:**
- `name contains 'keyword'` — filename search
- `mimeType = 'application/vnd.google-apps.document'` — Google Docs only
- `mimeType = 'application/pdf'` — PDFs only
- `'FOLDER_ID' in parents` — files in a specific folder
- `modifiedTime > '2026-06-01'` — recently modified

---

### 📂 "List what's in a Drive folder"

```
list_drive_items(folder_id="1o1mn51Vrgm1esCCrizaphG7GCElJk91C", user_google_email="naudiac@gmail.com")
```

**Key folder IDs:**

| Folder | ID |
|---|---|
| Gemini Experiments | `1o1mn51Vrgm1esCCrizaphG7GCElJk91C` |
| _Agent_Skills & Toolkits | `1MFSnh6nzlyNALcNn80RKUnOBW7hc_JYJ` |
| Assets & Archives | `1ubH_4V6GYsn-vKPeWdIMYmD9fhzprgtc` |
| Prompts & Blueprints | `1UUcypKzPWG_xpE0Q71ALduWPurXB6YKt` |
| Automation Vault | `1-yyV-8WgG4uGgweXv_BRiCUwtm5VY953` |
| Business Plans | `15r499_HYaRFI5bvOhOY9FKPOuNOAcPXa` |
| Business Ideas | `1D1jser48PZ6DjifXEUVp_KkxBiGjLkQ1` |
| Project Folder | `1bskG3tQiRKXARbgLJbukOBYAVyvBb7J2` |
| Paystubs (Send to Kim) | `1bjbJJ6KJbuZ3AlOsTM2B3qOztA-zzYMs` |

---

### ☁️ "Save / upload a file to Drive"

**New file:**
```
create_drive_file(
  file_name="filename.ext",
  content="...file content...",
  folder_id="1MFSnh6nzlyNALcNn80RKUnOBW7hc_JYJ",
  user_google_email="naudiac@gmail.com"
)
```

**Update existing file:**
```
update_drive_file(
  file_id="...",
  content="...new content...",
  user_google_email="naudiac@gmail.com"
)
```

> **Default upload target** for AI tools/scripts/configs:
> `Gemini Experiments → _Agent_Skills & Toolkits` (`1MFSnh6nzlyNALcNn80RKUnOBW7hc_JYJ`)

---

## Error Handling

| Error | Likely Cause | Fix |
|---|---|---|
| MCP Error / context deadline exceeded | Token expired or server not started | Re-authenticate (see `google-workspaceMCP-setup`) |
| 401 Unauthorized | Token revoked | Re-authenticate |
| 403 Forbidden | Wrong account or scope | Confirm `user_google_email` is `naudiac@gmail.com` |
| Tool not found | Wrong tool name | Check Full Tool Reference below |

---

## Full Tool Reference

### Gmail

| Tool | Required Args | Notes |
|---|---|---|
| `search_gmail_messages` | `query`, `user_google_email` | Returns message IDs + thread IDs |
| `get_gmail_message_content` | `message_id`, `user_google_email` | Single message full content |
| `get_gmail_messages_content_batch` | `message_ids[]`, `user_google_email` | Batch fetch — prefer this over single |
| `get_gmail_thread_content` | `thread_id`, `user_google_email` | Full conversation thread |
| `get_gmail_threads_content_batch` | `thread_ids[]`, `user_google_email` | Batch thread fetch |
| `draft_gmail_message` | `to`, `subject`, `body`, `user_google_email` | Saves as draft |
| `send_gmail_message` | `to`, `subject`, `body`, `user_google_email` | Sends immediately |
| `list_gmail_labels` | `user_google_email` | All 77+ labels with IDs |
| `manage_gmail_label` | `user_google_email`, ... | Create/rename labels |
| `modify_gmail_message_labels` | `message_id`, `user_google_email` | Add/remove labels on a message |
| `batch_modify_gmail_message_labels` | `message_ids[]`, `user_google_email` | Bulk label operations |
| `list_gmail_filters` | `user_google_email` | All Gmail filters |
| `manage_gmail_filter` | `user_google_email`, ... | Create/delete filters |
| `get_gmail_attachment_content` | `message_id`, `attachment_id`, `user_google_email` | Download attachment |

### Drive

| Tool | Required Args | Notes |
|---|---|---|
| `search_drive_files` | `query`, `user_google_email` | Drive query syntax |
| `list_drive_items` | `user_google_email` | Root or `folder_id` |
| `get_drive_file_content` | `file_id`, `user_google_email` | Read text/doc content |
| `get_drive_file_download_url` | `file_id`, `user_google_email` | Get download link |
| `create_drive_file` | `file_name`, `content`, `user_google_email` | Upload new file |
| `update_drive_file` | `file_id`, `content`, `user_google_email` | Overwrite existing |
| `create_drive_folder` | `name`, `user_google_email` | Creates folder |
| `copy_drive_file` | `file_id`, `user_google_email` | Duplicate a file |
| `get_drive_shareable_link` | `file_id`, `user_google_email` | Returns share URL |
| `get_drive_file_permissions` | `file_id`, `user_google_email` | List permissions |
| `manage_drive_access` | `file_id`, `user_google_email`, ... | Share/restrict access |
| `set_drive_file_permissions` | `file_id`, `user_google_email`, ... | Set specific permissions |
| `check_drive_file_public_access` | `file_id`, `user_google_email` | Is file public? |
| `import_to_google_doc` | `file_id`, `user_google_email` | Convert to Google Doc |
| `import_to_google_sheets` | `file_id`, `user_google_email` | Convert to Sheets |
| `import_to_google_slides` | `file_id`, `user_google_email` | Convert to Slides |
