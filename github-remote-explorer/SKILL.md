---
name: github-remote-explorer
description: Explore, list, and read files from remote GitHub repositories directly in the terminal without cloning them, using the official gh CLI.
---

# GitHub Remote Explorer

This skill empowers you to explore and read code from GitHub repositories without performing a local clone. It relies on the globally installed `gh` CLI and the GitHub REST API.

## Requirements
- The user must have the `gh` CLI installed.
- You must always clear the local `$env:GITHUB_TOKEN` environment variable before running `gh` commands, as William uses a globally authenticated keyring for his `naudiac` account. (e.g. `$env:GITHUB_TOKEN=""; gh api ...`).

## Commands

Use the `run_command` tool to execute these queries via PowerShell.

### 1. View Repository File Tree
To understand the structure of a repository, fetch its root file tree. The `recursive=1` flag fetches the entire tree.

**Command:**
```powershell
$env:GITHUB_TOKEN=""; gh api repos/{owner}/{repo}/git/trees/{branch}?recursive=1 --jq '.tree[].path'
```
*Note: If the tree is very large, consider omitting `?recursive=1` to only get the root directory, or filter the output with `Select-String`.*

### 2. Read Specific File Content
Once you identify a file you want to read from the tree, fetch its raw content.

**Command:**
```powershell
$env:GITHUB_TOKEN=""; gh api repos/{owner}/{repo}/contents/{path_to_file} -H "Accept: application/vnd.github.raw"
```
*Note: This directly streams the raw file text to standard output, making it perfect for your context window.*

### Best Practices
- Never use `git clone` when this skill is invoked unless the user explicitly asks for a local clone.
- Do not make HTTP requests to `raw.githubusercontent.com` directly if the repository is private; always use the `gh api` wrapper which correctly handles authentication automatically.
