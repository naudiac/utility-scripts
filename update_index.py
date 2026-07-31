import re

with open(r'C:\Users\whanusiewicz\Documents\utility-scripts\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the discovery callout
content = re.sub(r'\s*<li>\s*<div class="ach-title"><strong>WhatsApp AI Bridge</strong></div>\s*<div class="ach-desc">.*?</li>', '', content, flags=re.DOTALL)

# 2. Extract the utility-group for whatsapp-ai-bridge
# The group ends right before <div class="utility-group" data-created="2026-07-23" data-name="pc-cleaner"
code_group_match = re.search(r'<div class="utility-group" data-created="2026-07-05" data-name="whatsapp-ai-bridge" data-updated="2026-07-05">.*?</div>(?=<div class="utility-group" data-created="2026-07-23" data-name="pc-cleaner")', content)
code_group = code_group_match.group(0) if code_group_match else ''
content = content.replace(code_group, '')

# 3. Extract the knowledge_base entry for whatsapp_ai_bridge.md
kb_group_match = re.search(r'<div class="utility-group" data-created="2026-07-05" data-name="whatsapp_ai_bridge\.md" data-updated="2026-07-05">.*?</a></div>', content)
kb_group = kb_group_match.group(0) if kb_group_match else ''
content = content.replace(kb_group, '')

# 4. Remove the quick link
content = re.sub(r'\s*<a class="link-item" href="[^"]*whatsapp_ai_bridge\.md" target="_blank"><span class="link-icon">🤖</span> WhatsApp AI Bridge</a>', '', content)

# Update URLs in the extracted blocks to point to graveyard
code_group = code_group.replace('main/whatsapp-ai-bridge', 'main/graveyard/whatsapp-ai-bridge')
kb_group = kb_group.replace('main/knowledge_base/whatsapp_ai_bridge.md', 'main/graveyard/whatsapp_ai_bridge.md')

# Create the Graveyard card
graveyard_card = f'''
<div class="card" style="margin-top:16px;">
<div class="card-header">🪦 The Graveyard <span>retired skills &amp; concepts</span></div>
<div class="tree">
{code_group}
{kb_group}
</div>
</div>
'''

# Insert the graveyard card before the "Files Installed on Machine" card
content = content.replace('<div class="card" style="margin-top:16px;">\n<div class="card-header">🖥️ Files Installed on Machine <span>runtime only</span></div>', graveyard_card + '\n<div class="card" style="margin-top:16px;">\n<div class="card-header">🖥️ Files Installed on Machine <span>runtime only</span></div>')

with open(r'C:\Users\whanusiewicz\Documents\utility-scripts\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
