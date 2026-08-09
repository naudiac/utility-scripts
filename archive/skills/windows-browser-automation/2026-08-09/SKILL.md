---
name: windows-browser-automation
description: "Decision tree and execution guides for Windows web automation. Defines when to use standard Headless mode (default) vs. Headful mode (Session 0 bypass for user visibility)."
---

# Windows Browser Automation: Headless vs. Headful

When tasked with web automation on Windows, you must choose the correct execution mode based on the user's prompt. 

## ⚖️ Decision Tree: Which mode to use?

**Use HEADLESS Mode (Default) IF:**
- The user just wants a task done (e.g., "scrape this site", "fill out this form").
- Speed, stability, and background execution are preferred.
- *Do not use any special bypasses. Use standard Puppeteer/MCP tools.*

**Use HEADFUL Mode (Visual Bypass) ONLY IF:**
- The user explicitly asks to watch the process (e.g., "headful", "let me see it", "on my screen").
- The automation requires visual debugging or human-in-the-loop CAPTCHA solving on the interactive desktop.

---

## 🚀 MODE 1: Headless Execution (Standard)
1. Use the standard `@modelcontextprotocol/server-puppeteer` or your default Puppeteer scripts.
2. No special configuration is needed. The browser will run invisibly in Session 0.

## 🖥️ MODE 2: Headful Execution (Session 0 Bypass)
Because agents run as background services in Session 0, native GUI spawns (even with `headless: false`) are invisible to the user. You MUST inject the browser into the interactive desktop.

### 1. Patch the Puppeteer MCP Server
The default Puppeteer MCP server hard-locks the viewport to 800x600. Before connecting, patch it to use `defaultViewport: null`:
- Locate the MCP server index file (e.g., `~/.npm-cache/_npx/.../node_modules/@modelcontextprotocol/server-puppeteer/dist/index.js`).
- Replace `puppeteer.launch({` with `puppeteer.launch({defaultViewport: null,`
- Replace `puppeteer.connect({` with `puppeteer.connect({defaultViewport: null,`

### 2. Launch Edge Interactively
Use the Windows Task Scheduler to bypass Session 0 and launch a clean, isolated Microsoft Edge instance directly onto the user's screen with a debugging port open.
Run the following PowerShell snippet:
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -Argument "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\edge_debug_profile_headful --start-maximized"
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
$task = New-ScheduledTask -Action $action -Principal $principal
Register-ScheduledTask -TaskName "AgyHeadfulEdge" -InputObject $task -Force | Out-Null
Start-ScheduledTask -TaskName "AgyHeadfulEdge"
Start-Sleep -Seconds 3
Unregister-ScheduledTask -TaskName "AgyHeadfulEdge" -Confirm:$false
```

### 3. Connect the Agent
Instruct your automation subagent to connect its Puppeteer instance directly to `http://127.0.0.1:9222`. 
*(Note: Edge will display a first-run "Welcome" pop-up. The subagent must bypass this cleanly by executing a direct `page.goto(TARGET_URL)` immediately upon connection.)*

### 4. Custom Scripting (Raw Node.js)
If for any reason you bypass the MCP server and write your own raw Node.js Puppeteer scripts to connect to the browser, you MUST include `defaultViewport: null` in your connection parameters.
- **Example:** `const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222', defaultViewport: null });`
- **Why:** If you omit this, standard Puppeteer behavior will immediately force an 800x600 viewport lock onto the open browser, completely breaking the visual render for the user. Never omit this parameter in Headful mode.
