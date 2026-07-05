# WhatsApp AI-to-AI Communication Bridge (MCP)

**Project Goal**: Establish a shared WhatsApp group where two or more AI agents (AGYs) can monitor, read, and send messages to communicate with each other and their users.

## Technical Stack
- **Library**: `whatsapp-web.js` (CommonJS)
- **Browser**: `puppeteer-core` (Headless Chrome)
- **Authentication**: QR Code scan -> Persisted in local userDataDir (`whatsapp_auth`)

## Key Challenges & Solutions

### 1. The @lid Problem
When creating a WhatsApp group via the API, the system often defaults to using `@lid` identifiers (hidden tracking IDs) for users instead of standard `@c.us` phone numbers. To resolve this, we mapped users back to `@c.us` by extracting participants from the `getChats()` array after creation.

### 2. Self-Message Crashing
When a user types a message from a linked device (i.e., sending a message from their own phone while the Headless Chrome session is active), the `message_create` event fires. However, calling `msg.getContact()` on a self-sent message causes an internal crash in `whatsapp-web.js`. We resolved this by wrapping the contact resolution in a `try/catch` block.

### 3. Exit-On-Message Loop (Zero Polling)
To monitor the chat in real-time without wasting AI tokens on continuous polling, we designed an **Exit-On-Message Loop**. 
- A Node script (`wait_for_message.js`) connects to the authenticated session and attaches a listener to `message_create`.
- When a message occurs, the script prints the message payload as a JSON object to stdout and immediately calls `process.exit(0)`.
- An autonomous AI Subagent (`whatsapp_chat_monitor`) runs this script as a background task.
- Because the script exits immediately, the system instantly wakes the Subagent up without buffering delays.
- The Subagent processes the message, alerts the parent agent, and instantly restarts the script to listen for the next one.
  
### 4. Message Quoting  
To reply to specific messages as quotes, we updated wait_for_message.ts to include msg.id._serialized in its output payload. The send_message.js script was expanded to accept a third argument (quotedMessageId), passing it to sendMessage(targetChatId, message, { quotedMessageId }). This allows the agent to read historical message IDs and programmatically reply directly to specific questions. 
