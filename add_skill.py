import re

html_path = r'C:\Users\whanusiewicz\Documents\utility-scripts\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''<div class="utility-group" data-created="2026-07-31" data-name="skill-graveyard-retirement" data-updated="2026-07-31"><div class="tree-row folder" style="cursor:default;"><span class="icon">🪦</span><span class="file-name">skill-graveyard-retirement/</span><span class="file-desc">Safely archives obsolete tools</span><div class="date-meta"><span>Est: 2026-07-31</span><span>Upd: 2026-07-31</span></div></div><a class="tree-row indent" href="https://github.com/naudiac/utility-scripts/blob/main/skill-graveyard-retirement/SKILL.md" target="_blank"><span class="icon">📄</span><span class="file-name">SKILL.md</span><span class="file-badge badge-md">MD</span></a></div>'''

# Insert at the end of the first .tree div (Repository Structure)
# Find the first </div></div></div> (end of the last utility group) and insert before the </div></div>
# A safer way: Find the Knowledge Base card header, and insert right before the closing </div>\n</div> that precedes it.
# The structure is: ...</div></div>\n</div>\n<div class="card" style="margin-top:16px;">\n<div class="card-header">📚 Knowledge Base

search_str = '</div></div>\n</div>\n<div class="card" style="margin-top:16px;">\n<div class="card-header">📚 Knowledge Base'
replacement = '</div></div>' + new_block + '\n</div>\n<div class="card" style="margin-top:16px;">\n<div class="card-header">📚 Knowledge Base'

if search_str in content:
    content = content.replace(search_str, replacement)
else:
    print("Could not find the injection point!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
