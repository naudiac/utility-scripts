---
name: skill-graveyard-retirement
description: >-
  Retires an obsolete Antigravity skill, plugin, or workflow. Moves the active
  code out of runtime into a graveyard directory, safely archives the source code 
  in the utility-scripts repository, and updates the public HTML documentation 
  so that nothing is permanently lost but the system is freed of clutter.
---

# Skill Graveyard Retirement

## Overview
Safely decommissions an Antigravity skill or plugin. Instead of deleting old scripts, this workflow preserves them in a designated "Graveyard" while completely deregistering them from the active agent runtime. It also manages updating the public-facing documentation.

## Dependencies
None.

## Quick Start
Trigger this skill when the user asks to "retire", "archive", or "graveyard" an existing skill or plugin.
Ensure you know the exact name of the folder before starting (e.g. `whatsapp-ai-bridge`).

## Workflow

### 1. Deregister from Antigravity Runtime
Move the target folder from its active location to the local graveyard so it will no longer be loaded by the agent.
Run this PowerShell command (adjust paths as needed depending on if it's a plugin or skill):
```powershell
mkdir -p C:\Users\whanusiewicz\.gemini\config\graveyard
Move-Item -Path C:\Users\whanusiewicz\.gemini\config\plugins\<TARGET_NAME> -Destination C:\Users\whanusiewicz\.gemini\config\graveyard\<TARGET_NAME> -Force
```

### 2. Archive the Source Code in Git
Move the source code and knowledge base markdown files in the `utility-scripts` repository to its `graveyard` folder.
```powershell
mkdir -p C:\Users\whanusiewicz\Documents\utility-scripts\graveyard
Move-Item -Path C:\Users\whanusiewicz\Documents\utility-scripts\<TARGET_NAME> -Destination C:\Users\whanusiewicz\Documents\utility-scripts\graveyard\<TARGET_NAME> -Force
Move-Item -Path C:\Users\whanusiewicz\Documents\utility-scripts\knowledge_base\<TARGET_NAME>.md -Destination C:\Users\whanusiewicz\Documents\utility-scripts\graveyard\<TARGET_NAME>.md -Force
```
*(Note: If the knowledge base file doesn't exist, ignore the error.)*

### 3. Update the UI (`index.html`)
The skill must be removed from the active sections of the HTML documentation and moved to the Graveyard card. Since parsing minified HTML safely is difficult, use the following Python script pattern.
Save this as `update_index.py` in the `utility-scripts` directory and execute it using `python update_index.py`. 
**(IMPORTANT: Replace `<TARGET_NAME>` inside the regex patterns with the actual name of the skill before running!)**

```python
import re

html_path = r'C:\Users\whanusiewicz\Documents\utility-scripts\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_name = "<TARGET_NAME>"
# Note: Ensure the python string operations match the exact names used in the HTML data attributes.
# Example: If target_name is 'whatsapp-ai-bridge', it handles data-name="whatsapp-ai-bridge"

# 1. Remove from Discovery Callout (if present)
content = re.sub(rf'\s*<li>\s*<div class="ach-title"><strong>[^<]*{target_name}[^<]*</strong></div>.*?</li>', '', content, flags=re.DOTALL | re.IGNORECASE)

# 2. Extract the utility-group for the target from the main tree
# This matches up to the next utility-group or the end of the tree.
code_group_match = re.search(rf'<div class="utility-group"[^>]*data-name="{target_name}"[^>]*>.*?</div>(?=<div class="utility-group"|</div>\s*</div>)', content, flags=re.DOTALL)
code_group = code_group_match.group(0) if code_group_match else ''
content = content.replace(code_group, '')

# 3. Extract any knowledge_base entry
kb_name = target_name.replace('-', '_') + ".md"
kb_group_match = re.search(rf'<div class="utility-group"[^>]*data-name="{kb_name}"[^>]*>.*?</a></div>', content, flags=re.DOTALL)
kb_group = kb_group_match.group(0) if kb_group_match else ''
content = content.replace(kb_group, '')

# 4. Remove any Quick Links
content = re.sub(rf'\s*<a class="link-item" href="[^"]*{kb_name}" target="_blank">.*?</a>', '', content, flags=re.DOTALL)

# Update URLs in the extracted blocks to point to graveyard
code_group = code_group.replace(f'main/{target_name}', f'main/graveyard/{target_name}')
kb_group = kb_group.replace(f'main/knowledge_base/{kb_name}', f'main/graveyard/{kb_name}')

# 5. Insert into the Graveyard card
# Search for the graveyard card and inject the extracted blocks into its tree
graveyard_tree_start = r'<div class="card-header">🪦 The Graveyard <span>retired skills &amp; concepts</span></div>\s*<div class="tree">'
if re.search(graveyard_tree_start, content):
    replacement = f'\g<0>\n{code_group}\n{kb_group}'
    content = re.sub(graveyard_tree_start, replacement, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
```

### 4. Commit and Push
Finally, commit the changes to the `utility-scripts` repository so the GitHub Pages site updates.
```powershell
cd C:\Users\whanusiewicz\Documents\utility-scripts
git add .
git commit -m "chore: retire <TARGET_NAME> to graveyard"
git push origin main
```

## Common Mistakes
- Not replacing the `<TARGET_NAME>` token inside the Python script before running it.
- Failing to move both the active runtime plugin/skill AND the source code in `utility-scripts`. Both must be archived.
