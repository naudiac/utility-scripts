---
name: phone-mirror
description: >-
  Orchestrates a bidirectional mirrored terminal session between the Windows PC
  and the Android phone (Termux) over Tailscale. Automatically syncs keys, checks
  firewall, pops open the host session on the PC, and connects the phone via ADB.
---

# Phone Mirror

## Overview
This skill orchestrates a real-time mirrored terminal session between the user's PC and their Android phone (named "Biggest"). It bypasses Windows OpenSSH conflicts by running a native `openssh-server` inside WSL on port `22222`. The connection is established via a reverse SSH tunnel directly to the WSL subsystem, providing a perfectly scaled, fully encrypted PTY. 

## Quick Start
"mirror my phone"
"launch the mirrored terminal"

## Workflow

### 1. Start the Secure Reverse Tunnel
- Ensure WSL's `sshd` is running and the tunnel is established:
  ```powershell
  wsl -u root service ssh start
  ssh -o StrictHostKeyChecking=no -N -R 3333:[::1]:22222 -p 8022 -i C:\Users\whanusiewicz\.gemini\antigravity\scratch\phone-cli\termux_rsa 192.168.4.83
  ```
- *Note:* This command must run asynchronously in the background.

### 2. Launch Host Session on PC
- Pop open a new PowerShell window on the user's monitor to host the tmux session:
  ```powershell
  Start-Process powershell -ArgumentList "-NoExit -Command wsl tmux new-session -A -s antigravity /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
  ```

### 3. Connect the Phone (Client)
- Ask the user to type `mirror` on their phone's Termux app, OR use the `phone-control` skill to push the text automatically.
- The `mirror` script on the phone is pre-configured to execute:
  `ssh -p 3333 -o StrictHostKeyChecking=no whanusiewicz@127.0.0.1 -t "tmux attach -t antigravity"`

## Troubleshooting
- If `can't find session: antigravity` appears, the host `tmux` session on the PC hasn't been started yet (Step 2).
- If `Connection refused` appears, the background reverse tunnel from Step 1 has dropped and needs to be restarted.
