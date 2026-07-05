# System Monitor Bridge

This repository contains the local bridge node that connects the terminal agent instance to WhatsApp via WhatsApp-Web.js.

## Prerequisites
- Node.js (v18+)
- PowerShell (for the tripwire script)

## Setup

1. **Install Dependencies**
   Run the following command to install the required Node modules:
   ```bash
   npm install
   ```

2. **Configure Environment Variables**
   Create a `.env` file in this directory and populate it with your contact name (or base ID) to whitelist yourself for authorized commands:
   ```env
   ADMIN_WHITELIST="Your Name, Your Alias"
   ```
   *Only messages from these users starting with `/`, `AGY`, or `@AGY` will trigger the tripwire.*

3. **Build the Bridge**
   Compile the TypeScript code:
   ```bash
   npm run build
   ```

4. **Run the Bridge**
   Start the monitor, replacing `<CHAT_ID>` with the specific WhatsApp Chat ID you want to monitor (e.g. `123456789@g.us` for a group, or `123456@c.us` for a direct message):
   ```bash
   node dist/smart_monitor.js <CHAT_ID>
   ```

5. **Arm the Tripwire**
   In a separate PowerShell window, run the zero-latency tripwire monitor. This script alerts the AI when an authorized command is detected:
   ```powershell
   ./run_tripwire.ps1
   ```

## Architecture
- **smart_monitor.js**: The main event loop that uses `whatsapp-web.js` to listen for messages. It logs authorized commands to `tripwire.txt` and maintains a full memory log in `chat_history.txt`.
- **Local API Server**: An Express server runs on port 3000 to allow the AI to send messages and change group icons via REST POST requests.
- **Backlog Processing**: On startup, the bridge fetches the last 50 messages and processes any missed authorized triggers.
