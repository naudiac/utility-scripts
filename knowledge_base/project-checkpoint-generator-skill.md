---
name: project-checkpoint-generator
description: Creates a standardized markdown savepoint for long-running, complex projects to anchor state, document infrastructure shifts, and enable clean context recovery across sessions.
---

# Project Checkpoint Generator

Use this skill when the user explicitly asks to create a "checkpoint" or "savepoint", OR proactively suggest it when a major project phase or version iteration (e.g., V10 -> V11) is completed.

## Why Checkpoints are Needed
In long-running development tasks, conversation logs get truncated and context is lost. Checkpoints act as a hard anchor that a future agent can read to instantly understand the current state of the codebase, which scripts are active, and what bugs were just solved.

## Workflow
1. **Identify the Workspace**: Determine the primary directory where the project is housed.
2. **Determine the Filename**: Name the file `project_checkpoint_[phase_or_version].md` (e.g., `project_checkpoint_v70.md` or `project_checkpoint_phase3.md`).
3. **Generate the Content**: Write the checkpoint using the **Standard Format** below.
4. **Save**: Save the file directly into the project's working directory.

## Standard Format

```markdown
# [Project Name] - [Version/Phase] Checkpoint

**Date:** [Current Date]
**Current Phase:** [Name of Phase]
**Current Version:** [Version Number]

## 1. Project Status & Updates
Briefly summarize the evolution up to this point.
**Key Achievements in [Version]:**
1. [Achievement 1]
2. [Achievement 2]

## 2. Infrastructure & Build Pipeline Shifts
Note any major changes in how the code is built, compiled, or tested (e.g., "Switched from Python scripts to PowerShell for JSON injection").

## 3. Key Artifacts
List the absolute paths to the essential files driving the current state of the project, along with a 1-sentence description of their purpose.
- `path/to/main_script.cs`: Handles core logic.
- `path/to/build_tool.ps1`: Compiles the template.

## 4. Key Conversations & Context
List critical previous Conversation IDs that contain important context, design decisions, or roadblocks for this phase. This allows future agents to search the `transcript.jsonl` files to recover granular reasoning.
- `Conversation ID: 9872bd78...`: Solved the SQL fallback logic and UI pill CSS.
- `Conversation ID: 4122bc12...`: Initial discovery of the ThinkAutomation JSON injection bug.

## 5. Current Objectives & Next Steps
1. [Next step 1]
2. [Next step 2]
```
