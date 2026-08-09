---
name: mobile-linkedin-navigator
description: Safely navigates the LinkedIn Android app natively via ADB and vision to bypass aggressive web anti-bot defenses.
---

# Mobile LinkedIn Navigator

## Overview
LinkedIn aggressively blocks web scrapers and Puppeteer instances, often resulting in immediate timeouts or CAPTCHAs. This skill defines the mandatory workflow for interacting with LinkedIn by driving William's Android phone (Galaxy S24 Ultra, 1440x3120) over an ADB bridge and using LLM vision capabilities to read the screen.

## Core Directives
1. **Never use Puppeteer/Chrome for LinkedIn.** Any request to read or update LinkedIn MUST route through the Android ADB bridge.
2. **Never attempt to fetch HTML.** Always use `screencap` and read the visual output.
3. **Be Patient.** Mobile UI transitions take time. Always wait 2-3 seconds after a swipe or tap before taking the next screenshot.

## Interaction Primitives
Execute these via the `run_command` tool in PowerShell.

### 1. Take a Screenshot
Capture the current screen and save it to the current artifact directory for vision analysis.
```powershell
cmd.exe /c "C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat exec-out screencap -p > C:\Users\whanusiewicz\.gemini\antigravity-cli\brain\<conversation-id>\cell_ss_N.png"
```
*(Always use `view_file` to read the resulting image.)*

### 2. Scroll/Swipe Down
Scrolls the view down to reveal more content.
```powershell
C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat shell input swipe 500 2000 500 500 500
```

### 3. Tap an Element
When you identify a button (e.g., "See more", "Add Certification") in the screenshot, estimate its X/Y coordinates based on the 1440x3120 resolution and tap it.
```powershell
C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat shell input tap <X> <Y>
```

### 4. Enter Text
To fill out a form (e.g., adding a certification name).
```powershell
C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat shell input text "Text%sto%stype"
```
*(Note: Replace spaces with `%s` when using `input text`)*

## Chaining Commands
For efficiency, chain the action, a wait, and the next screenshot into a single `run_command` call:
```powershell
C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat shell input swipe 500 2000 500 500 500 ; Start-Sleep -Seconds 2 ; cmd.exe /c "C:\Users\whanusiewicz\.gemini\antigravity\scratch\adb.bat exec-out screencap -p > C:\Users\whanusiewicz\.gemini\antigravity-cli\brain\<conversation-id>\cell_ss_next.png"
```

## CargoWise Certification Update Protocol (Future Workflow)
When tasked with updating William's LinkedIn with new CargoWise certifications:
1. Retrieve the certification details via the `cargowise-database-query` skill.
2. Launch/focus the LinkedIn app via ADB.
3. Navigate to the Profile -> Certifications section.
4. Tap the "+" (Add) button.
5. Use `input text` to fill in the certification name and issuing organization (WiseTech Global).
6. Tap "Save".
7. Verify success via a final screenshot.
