---
name: thinkautomation-iteration-guide
description: Strict checklist and workflow for creating new iterations of the ThinkAutomation Phase 2 project. Trigger whenever asked to create a new version (e.g., v76 to v77).
---

# ThinkAutomation Iteration Workflow

When asked to create a new version (e.g., moving from `vX` to `vY`), you must strictly follow this checklist to prevent ghost strings, broken paths, and Studio warnings.

## 1. File Duplication
Copy the following files from the previous iteration (`vX`):
- `new_routing_script_vX.cs` -> `new_routing_script_vY.cs`
- `build_vX.py` -> `build_vY.py`
- `build_gallery_vX.py` -> `build_gallery_vY.py`
- `test_sequence_vX.txt` -> `test_sequence_vY.txt`

## 2. Build Script Pathing
Update `build_vY.py`:
- The input JSON MUST point to the previous version (`vX.json`). Do not accidentally point it to `vY.json`.
- The output JSON MUST point to `vY.json`.
- The script target MUST point to `new_routing_script_vY.cs`.

## 3. Scrub Ghost Versions (JSON & C#)
When bumping versions, it is critical that ALL references are updated:
- **Python Build Script**: Ensure `build_vY.py` has a recursive string replacement loop that catches strings like `Version X` and `(vX)` and replaces them with `Version Y` and `(vY)`. This ensures that ThinkAutomation UI action nodes (like Comments and Email Subjects) don't carry over old version numbers.
- **C# Script**: Scrub `new_routing_script_vY.cs` for any internal log statements (e.g., `message.AddToLog("Phase 3 V70...")`) or comments that mention the old version.

## 4. ThinkAutomation Variable Escape Hack
ThinkAutomation's C# editor runs a static analyzer that throws warnings if it sees raw `%VariableName%` strings that haven't been declared in the flow. 
- **Rule**: NEVER write literal variables like `message.GetValue("%Msg_FromAddress%")`.
- **Fix**: ALWAYS evade the parser using string concatenation: `message.GetValue("%" + "Msg_FromAddress" + "%")`.
