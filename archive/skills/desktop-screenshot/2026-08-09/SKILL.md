---
name: desktop-screenshot
description: Captures and views a screenshot of the user's primary Windows desktop monitor, bypassing background service session isolation. Trigger when the user asks to see their screen or desktop.
---

# Desktop Screenshot Skill

When the user asks you to look at their screen or desktop, you must use this specific workaround to capture it. Because you run as a background agent, running standard screenshot commands (like `nircmd` or PowerShell `CopyFromScreen`) directly via `run_command` will result in a black image or an invalid handle error due to Window Station isolation.

To capture the actual visible desktop, use a temporary Scheduled Task to launch `nircmd` in the interactive user session.

### Execution Steps

1. **Run the Workaround Command**:
   Use the `run_command` tool to execute the following PowerShell script exactly as written. This creates an interactive scheduled task, runs it, waits 3 seconds, and then deletes it. Set `WaitMsBeforeAsync` to `5000` (5 seconds).

   ```powershell
   $action = New-ScheduledTaskAction -Execute "C:\Users\whanusiewicz\bin\nircmd.exe" -Argument 'savescreenshot "C:\Users\whanusiewicz\desktop_screen.png"'
   $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
   $task = New-ScheduledTask -Action $action -Principal $principal
   Register-ScheduledTask -TaskName "AgyScreenshot" -InputObject $task -Force | Out-Null
   Start-ScheduledTask -TaskName "AgyScreenshot"
   Start-Sleep -Seconds 3
   Unregister-ScheduledTask -TaskName "AgyScreenshot" -Confirm:$false
   ```

2. **View the File**:
   Once the command completes, use your `view_file` tool on `C:\Users\whanusiewicz\desktop_screen.png` to analyze the screenshot.

3. **Respond**:
   Describe what you see on the screen to the user based on their original request.
