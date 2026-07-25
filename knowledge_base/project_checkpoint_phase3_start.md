# ThinkAutomation AP Routing - Phase 3 Checkpoint

**Date:** July 25, 2026
**Current Phase:** Phase 3 (Initiated)
**Current Version:** V18

## 1. Project Status & V18 Updates
Phase 2 successfully proved the core architecture (Regex extraction + SQL replica resolution). However, the battery test revealed a critical blind spot with image-based flatbed scan PDFs. 
**V18 has been generated to fix this by introducing a dual-layer extraction model:**
1. **Native Text Layer:** Handled by `PDFConvert`. Lightning fast, 100% accurate for digital PDFs.
2. **Optical Text Layer:** Handled by `DocumentOCR`. Catches scanned PDFs (`*.pdf`) and invoice photos (`*.jpg`, `*.png`).
3. **Image Conversion:** Converts flat images into standard PDFs for the Ops team before forwarding.
4. **Junk Filtering:** Explicitly omits `*.gif` files to prevent email signatures and tracking pixels from cluttering the pipeline.

## 2. Adaptive Testing Methodology (The "Toolbox" Strategy)
Going forward, we will dynamically select our testing environment based on the specific challenge at hand, ensuring the fastest and most accurate feedback loops:

- **Live End-to-End Testing (The ThinkAutomation Engine):**
  - *When to use:* Testing proprietary ThinkAutomation components (e.g., DocumentOCR performance, email forwarding, attachment handling).
  - *How:* Loading the JSON into the actual ThinkAutomation studio and running live inbox tests (`battery_test.ps1`).

- **The C# Sandbox (Rapid Logic Iteration):**
  - *When to use:* Developing and testing Phase 3 Regex patterns, vendor logic, and CargoWise SQL queries.
  - *How:* A standalone local C# test harness that executes our script against dummy data, completely bypassing ThinkAutomation to provide millisecond feedback loops.

## 3. Key Artifacts
- **[ThinkAutomation_Phase2_TEST_MODE_v18.json](file:///C:/Users/whanusiewicz/Desktop/ThinkAutomation_Phase2_Backup/ThinkAutomation_Phase2_TEST_MODE_v18.json):** The current trigger logic containing the dual-layer extraction.
- **[battery_test.ps1](file:///C:/Users/whanusiewicz/Desktop/ThinkAutomation_Phase2_Backup/battery_test.ps1):** The automated PowerShell simulation script (Timeout increased to 180s to accommodate heavy OCR).
- **[modify_json_test_v18.py](file:///C:/Users/whanusiewicz/Desktop/ThinkAutomation_Phase2_Backup/modify_json_test_v18.py):** The Python script that generated V18.

## 4. Phase 3 Objectives
1. **Validate V18:** Confirm the optical layer successfully extracts text from scanned PDFs (like `email12`) via live testing.
2. **Build Sandbox:** Stand up the local C# test harness.
3. **Vendor Routing & Fallbacks:** Implement rules for when SQL finds references but returns zero active operators (e.g., `email7`).
4. **Attachment Size Filtering:** Strip small images (signatures/logos) before forwarding to Ops.
