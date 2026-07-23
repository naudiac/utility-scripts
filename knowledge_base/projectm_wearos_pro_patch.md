# projectM Wear OS Pro Patch & 10,000+ Preset Deployment

## Executive Summary

This document details the engineering solution for deploying **projectM Music Visualizer** onto the **Samsung Galaxy Watch 5 Pro (SM-R920)**, unlocking Pro features, neutralizing upgrade nag screens, and expanding the visualizer library from 347 to 10,000+ Milkdrop presets.

---

## 1. Play Store Compatibility Bypass

### Problem
When opening the Play Store page for `com.psperl.projectM` on Wear OS, Google Play displays:  
> *"Your device is not compatible with this version."*

### Cause
The Play Store package manifest omits Wear OS target tags (`android.hardware.type.watch`) and distributes split APK bundles (`split_config.arm64_v8a.apk`) designed exclusively for 64-bit phones.

### Solution
Deploy the universal multi-architecture release (`nodpi`) over Wi-Fi ADB. The universal APK contains `lib/armeabi-v7a/libprojectM.so`, providing native 32-bit C++ rendering support for the Galaxy Watch 5 Pro CPU (`SM-R920`).

---

## 2. Bytecode Modification & Pro Unlock

### Problem
When sideloading `com.psperl.prjM`, the app checks Google Play Billing. Upon receiving `RESULT_BILLING_UNAVAILABLE`, it triggers `showUpgradeDialog()` and `showUpgradeToast()` popups, locking Pro visualizer options.

### Failure Analysis of Direct Binary String Patching
Initial attempts to patch DEX byte strings directly using Python resulted in runtime crashes:
```
FATAL EXCEPTION: main
java.lang.RuntimeException: Unable to get provider com.psperl.prjM.providers.PresetsContentProvider:
java.lang.ClassNotFoundException: Didn't find class "com.psperl.prjM.providers.PresetsContentProvider" on path: DexPathList[[zip file "/data/app/.../base.apk"]]
```
**Root Cause**: String replacements shifted offsets in `classes2.dex`, causing `BaseDexClassLoader` to reject `classes2.dex`. Because `PresetsContentProvider` resided in `classes2.dex`, the app crashed on launch.

### Smali Decompilation Fix
Using `apktool`, `classes2.dex` was decompiled to Smali assembly and modified cleanly:

1. **`smali_classes2/com/psperl/prjM/MainActivity.smali`**:
   - `.method locked()Z` — Changed return value to always return `false` (`0x0`):
     ```smali
     .method locked()Z
         .locals 1

         const/4 v0, 0x0

         return v0
     .end method
     ```
   - `.method private showUpgradeDialog()V` — Changed to return `void` immediately:
     ```smali
     .method private showUpgradeDialog()V
         .locals 0

         return-void
     .end method
     ```

2. **`smali_classes2/com/psperl/prjM/util/BillingUtils.smali`**:
   - `.method public static isOldAppInstalled(Landroid/content/pm/PackageManager;)Z` — Changed to always return `true` (`0x1`):
     ```smali
     .method public static isOldAppInstalled(Landroid/content/pm/PackageManager;)Z
         .locals 1

         const/4 v0, 0x1

         return v0
     .end method
     ```

---

## 3. Android R+ Zip Alignment & Signing

### Android R+ Alignment Requirement
During `adb install`, Android 11+ (SDK 30+) enforces strict zip alignment rules:
```
Failure [-124: Failed parse during installPackageLI: Targeting R+ (version 30 and above) requires the resources.arsc of installed APKs to be stored uncompressed and aligned on a 4-byte boundary]
```

### Build Rules
1. In `zipfile` packaging:
   - Keep `lib/*.so` AND `resources.arsc` **STORED uncompressed** (`ZIP_STORED`).
   - Compress remaining assets (`ZIP_DEFLATED`).
2. Run `uber-apk-signer.jar --apks <apk> --overwrite` to generate aligned v1 + v2 + v3 RSA signatures.

---

## 4. 10,000+ Preset Deployment Architecture

- **GitHub Preset Source**: `projectM-visualizer/presets-cream-of-the-crop` (9,795 presets)
- **GitHub Texture Source**: `projectM-visualizer/presets-milkdrop-texture-pack` (66 textures)
- **Target Storage Directory**:  
  - Phone: `/sdcard/Android/data/com.psperl.projectM/files/presets_dir/`  
  - Watch: `/sdcard/Android/data/com.psperl.prjM/files/presets_dir/`  
- **Batch Transfer Protocol**: Single `combined_presets.zip` compressed archive pushed via ADB (2.5s transfer speed) and extracted in-place using Android `/system/bin/unzip`.

---

## 5. Verification
- **ADB Logcat Verification**: Verified clean startup without any `AndroidRuntime` exceptions or `ClassNotFoundException`.
- **UI Verification**: Galaxy Watch app opens directly to fullscreen visualizer with zero upgrade prompts or billing dialogs.
