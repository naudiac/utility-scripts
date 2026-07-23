# projectM Phone & Watch Sync Engine

Automated deployment tool & bytecode modification pipeline for **projectM Music Visualizer** across Android Phones (Samsung Galaxy S24 Ultra) and Wear OS Smartwatches (Samsung Galaxy Watch 5 Pro).

## Key Features

1. **Massive Preset Expansion**:
   - Downloads the official **[projectM-visualizer/presets-cream-of-the-crop](https://github.com/projectM-visualizer/presets-cream-of-the-crop)** (9,795 Milkdrop presets).
   - Downloads the official **[projectM-visualizer/presets-milkdrop-texture-pack](https://github.com/projectM-visualizer/presets-milkdrop-texture-pack)** (66 shader textures).
   - Auto-packages and pushes directly to Android app storage (`presets_dir`), expanding active visualizer rotation from **347 → 10,000+ presets**.

2. **Wear OS Compatibility & Bytecode Patching**:
   - Resolves Google Play Store "Device incompatible" blocks by deploying universal multi-architecture builds (`armeabi-v7a` support for smartwatch hardware).
   - Uses `apktool` to decompile `smali_classes2` and patches bytecode:
     - `MainActivity.smali` (`locked()Z` → always return `false`, unlocking Pro features).
     - `MainActivity.smali` (`showUpgradeDialog()` → `return-void`, eliminating upgrade popups).
     - `BillingUtils.smali` (`isOldAppInstalled()` → return `true`).
   - Ensures Android R+ compliance by keeping `resources.arsc` and `lib/*.so` uncompressed (`ZIP_STORED`).
   - Re-signs with `uber-apk-signer` using valid v1 + v2 + v3 Android RSA signatures.

## Quick Usage

```powershell
# Sync 10,000+ presets to both Phone and Galaxy Watch over Wi-Fi ADB
.\Sync-ProjectM.ps1 -Target Both
```

## Knowledge Base Reference
See `knowledge_base/projectm_wearos_pro_patch.md` for complete technical details, logcat crash analyses, and bytecode modification patterns.
