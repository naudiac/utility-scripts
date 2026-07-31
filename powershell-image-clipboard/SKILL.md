---
name: powershell-image-clipboard
description: >-
  Copies a local image file directly to the Windows clipboard using System.Windows.Forms.Clipboard so it can be pasted into rich text apps.
---

# PowerShell Image Clipboard

## Overview
This skill provides a simple PowerShell script to load a local image file (like a `.png` or `.jpg`) and push its pixel data directly into the Windows clipboard. This bypasses the issues with the standard `Set-Clipboard` command, which often fails to format image data correctly for pasting into chat applications or rich text editors on modern Windows versions.

## Quick Start
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\whanusiewicz\.gemini\config\skills\powershell-image-clipboard\scripts\copy_to_clipboard.ps1 -ImagePath "C:\path\to\image.png"
```

## Utility Scripts

### `copy_to_clipboard.ps1`
Loads an image and copies it to the clipboard.

**Arguments:**
- `-ImagePath` (required): Absolute path to the local image file.

**Example:**
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\whanusiewicz\.gemini\config\skills\powershell-image-clipboard\scripts\copy_to_clipboard.ps1 -ImagePath "C:\Users\whanusiewicz\desktop_screen.png"
```

## Common Mistakes
- Don't try to use `cat image.png | Set-Clipboard` or generic PowerShell commands, as they won't put the proper OLE object into the clipboard for images. Always use this script!
