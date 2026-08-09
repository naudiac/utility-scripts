---
name: image-grid-overlay
description: >-
  Draws a labeled coordinate grid over an image for precise pixel extraction. Useful for UI manipulation or cropping when bounding boxes aren't available.
---

# Image Grid Overlay

## Overview
This skill provides a helper script that takes an image file and draws a labeled horizontal coordinate grid over it (every 20 pixels by default). This makes it extremely easy to read exact Y-pixel coordinates from an image for precise cropping, stitching, or interacting with UI elements visually when no DOM or text bounding boxes are available.

## Quick Start
To draw a grid on a screenshot:
```powershell
uv run C:\Users\whanusiewicz\.gemini\config\skills\image-grid-overlay\scripts\draw_grid.py --input C:\path\to\image.png --output C:\path\to\grid.png
```

Then use the `view_file` tool on `grid.png` to inspect the exact coordinates.

## Utility Scripts

### `draw_grid.py`
Draws a coordinate grid over an image.

**Arguments:**
- `--input` (required): Path to the input image.
- `--output` (required): Path to save the new image with the grid overlay.
- `--spacing` (optional): Grid line spacing in pixels. Default is 20.

**Example:**
```powershell
uv run C:\Users\whanusiewicz\.gemini\config\skills\image-grid-overlay\scripts\draw_grid.py --input desktop_screen.png --output desktop_grid.png --spacing 50
```

## Common Mistakes
- Trying to rely on heuristic row-brightness or OCR for precise image cropping often fails due to anti-aliasing, non-uniform backgrounds, or missing dependencies. Always use this grid overlay to find the exact coordinates first!
