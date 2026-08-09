---
name: william-dual-monitor-wallpaper
description: Use when the user asks to generate, update, or create a background/wallpaper for their dual monitors. This skill handles the unique physical layout of William's screens.
---

# Dual Monitor Wallpaper Generation for William

William has a unique dual-monitor setup:
- **Screen 1 (Primary, Left)**: 1920x1080 Landscape. Bounding Box: `X=0, Y=0, W=1920, H=1080`.
- **Screen 2 (Secondary, Right)**: 1080x1920 Portrait. Bounding Box: `X=1920, Y=-455, W=1080, H=1920`.

Due to this layout, standard spanning or mirroring does not work. You must follow these exact steps to create a seamless mural:

## Step 1: Generate a 3:2 Master Image
Use the `generate_image` tool to create a large master image. 
- You MUST set `AspectRatio: "3:2"`.
- Ensure the composition places important elements appropriately (e.g., if the user wants something on Screen 2, keep in mind Screen 2 is the right-hand slice).

## Step 2: Slice and Set the Wallpaper
Once you have the generated image path, run the following PowerShell script via the `run_command` tool. Replace `$MASTER_IMAGE_PATH` with the path to the newly generated image. This script will automatically scale the master image, slice it for the exact monitor coordinates, and set the wallpapers using the `IDesktopWallpaper` API.

```powershell
$MASTER_IMAGE_PATH = "REPLACE_WITH_IMAGE_PATH"
$SCREEN1_OUT = "$env:TEMP\screen1_wallpaper.jpg"
$SCREEN2_OUT = "$env:TEMP\screen2_wallpaper.jpg"

# 1. Python script to slice the image
python -c "
from PIL import Image
im = Image.open(r'$MASTER_IMAGE_PATH')
im = im.resize((3000, 2000), Image.Resampling.LANCZOS)
im_virtual = im.crop((0, 40, 3000, 1960))
screen1 = im_virtual.crop((0, 455, 1920, 1535))
screen1.save(r'$SCREEN1_OUT')
screen2 = im_virtual.crop((1920, 0, 3000, 1920))
screen2.save(r'$SCREEN2_OUT')
"

# 2. Reset Windows span/tile settings to avoid conflicts
Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name WallpaperStyle -Value 10
Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name TileWallpaper -Value 0

# 3. C# Script to set individual wallpapers
$code2 = @'
using System;
using System.Runtime.InteropServices;
public class WallpaperSetter {
    [ComImport]
    [Guid(""C2CF3110-460E-4fc1-B9D0-8A1C0C9CC4BD"")]
    public class DesktopWallpaper { }
    [ComImport]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    [Guid(""B92B56A9-8B55-4E14-9A89-0199BBB6F93B"")]
    public interface IDesktopWallpaper {
        void SetWallpaper([MarshalAs(UnmanagedType.LPWStr)] string monitorID, [MarshalAs(UnmanagedType.LPWStr)] string wallpaper);
        [return: MarshalAs(UnmanagedType.LPWStr)] string GetWallpaper([MarshalAs(UnmanagedType.LPWStr)] string monitorID);
        [return: MarshalAs(UnmanagedType.LPWStr)] string GetMonitorDevicePathAt(uint monitorIndex);
        uint GetMonitorDevicePathCount();
        void GetMonitorDeviceRect([MarshalAs(UnmanagedType.LPWStr)] string monitorID, out int displayRect);
        void SetBackgroundColor(uint color);
        uint GetBackgroundColor();
        void SetPosition(int position);
    }
    public static void Set(uint monitorIndex, string path) {
        var desktopWallpaper = (IDesktopWallpaper)new DesktopWallpaper();
        string monitorId = desktopWallpaper.GetMonitorDevicePathAt(monitorIndex);
        desktopWallpaper.SetPosition(4); // Fill
        desktopWallpaper.SetWallpaper(monitorId, path);
    }
}
'@
Add-Type -TypeDefinition $code2
[WallpaperSetter]::Set(0, $SCREEN1_OUT)
[WallpaperSetter]::Set(1, $SCREEN2_OUT)
```

## Step 3: Wait for completion
Wait for the command to complete successfully, then inform the user that the new dual-monitor mural is ready.
