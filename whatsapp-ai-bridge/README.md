# WhatsApp AI Bridge

A real-time, event-driven bridge between WhatsApp (via `whatsapp-web.js`) and agentic LLMs. 
It features a Zero-Latency Tripwire architecture that allows an AI sandbox (like Antigravity) to remain asleep until a specific trigger is detected, saving compute costs and avoiding API rate limits in busy group chats.

## Architecture

1. **Node.js Monitor (`smart_monitor.ts`)**: Runs in the background and silently logs all messages, edits, and deletions to a local `chat_history.txt` file. 
2. **Zero-Latency Tripwire (`tripwire.txt`)**: When the Node.js monitor detects an explicit AI trigger (e.g., `/`, `AGY`, or `@AGY`) from an *authorized user*, it touches a file called `tripwire.txt`.
3. **PowerShell Watcher (`run_tripwire.ps1`)**: A lightweight script running in the AI's sandbox loop. It instantly detects the tripwire file, deletes it, and exits. This immediately wakes up the AI.
4. **AI Processing**: The AI reads the `chat_history.txt` file to gain full context of the conversation, generates a response, and sends it back to WhatsApp via a local Express API (`POST http://localhost:3000/send`).

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Whitelist**
   Copy `.env.example` to `.env` and set the authorized users who are allowed to trigger the AI:
   ```bash
   ADMIN_WHITELIST="William Hanusiewicz,Sal"
   ```

3. **Build TypeScript**
   ```bash
   npm run build
   ```

## Usage

1. **Start the Background Monitor**
   ```bash
   node dist/smart_monitor.js <Your_Group_Chat_ID@g.us>
   ```
   *On first run, it will print a QR code in the terminal. Scan this with the WhatsApp app on your phone to link the device.*

2. **Arm the Tripwire (AI Sandbox Side)**
   In your AI sandbox environment (e.g. Antigravity), run:
   ```powershell
   ./run_tripwire.ps1
   ```
   *The AI will suspend execution until the tripwire is triggered.*
