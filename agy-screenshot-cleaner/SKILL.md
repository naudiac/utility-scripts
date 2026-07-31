---
name: agy-screenshot-cleaner
description: >-
  Framework and instructions for cleaning up Antigravity CLI screenshots by cropping out agent thinking blocks and seamlessly stitching the conversation back together.
---

# AGY Screenshot Cleaner

## Overview
This skill provides the exact workflow and helper script needed to take a raw screenshot of an Antigravity CLI conversation, remove the distracting "Thought" and tool-usage blocks, and stitch the conversation perfectly back together. 

It prevents the need for manual cropping or unreliable OCR/brightness heuristics.

## Dependencies
- **desktop-screenshot**: Needed to capture the original screen without being blocked by background isolation.
- **image-grid-overlay**: Needed to precisely find the pixel Y-coordinates of the regions to keep.
- **powershell-image-clipboard**: Needed to copy the final stitched image to the user's clipboard.

## Quick Start
```powershell
uv run C:\Users\whanusiewicz\.gemini\config\skills\agy-screenshot-cleaner\scripts\stitch_screenshot.py --input raw_screen.png --output clean_screen.png --keep-ranges "0-40" "285-545" "683-1030"
```

## Workflow

When the user asks you to take a clean screenshot of the conversation:

### 1. Capture the Screen
Run the `desktop-screenshot` skill exactly as instructed to generate the `desktop_screen.png` file.

### 2. Generate a Grid Overlay
Use the `image-grid-overlay` script to draw horizontal coordinate lines over the screenshot:
```powershell
uv run C:\Users\whanusiewicz\.gemini\config\skills\image-grid-overlay\scripts\draw_grid.py --input C:\Users\whanusiewicz\desktop_screen.png --output C:\Users\whanusiewicz\grid_screen.png --spacing 20
```

### 3. Read Coordinates
Use the `view_file` tool on `grid_screen.png` to visually identify the EXACT `y` coordinate ranges of the sections you want to KEEP. (e.g., keep the title bar, keep the user prompts, keep the agent's final markdown response text). Write down these pairs (e.g. `0-40`, `285-545`, etc).

### 4. Stitch the Image
Run the stitch script to crop out all the unlisted rows and fuse the kept rows together vertically:
```powershell
uv run C:\Users\whanusiewicz\.gemini\config\skills\agy-screenshot-cleaner\scripts\stitch_screenshot.py --input C:\Users\whanusiewicz\desktop_screen.png --output C:\Users\whanusiewicz\clean_screen.png --keep-ranges "0-40" "285-545" "683-1030"
```

### 5. Copy to Clipboard
Use the clipboard skill to send the final image directly to the user's clipboard for pasting:
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\whanusiewicz\.gemini\config\skills\powershell-image-clipboard\scripts\copy_to_clipboard.ps1 -ImagePath "C:\Users\whanusiewicz\clean_screen.png"
```

## Common Mistakes
- **Guessing Coordinates**: Never guess the Y-coordinates or try to parse them with Python brightness checks. It fails on anti-aliased text. Always generate and view the grid overlay.
- **Skipping the Horizontal Rules**: Try to preserve the horizontal dividing lines between prompts for a natural look.
