import { waManager } from "./whatsappClient.js";
import * as fs from 'fs';
import * as path from 'path';
import express from 'express';

const app = express();
app.use(express.json());

const ID_FILE = path.join(process.cwd(), 'last_processed_msg_id.txt');

async function getSavedMsgId(): Promise<string | null> {
    try {
        if (fs.existsSync(ID_FILE)) {
            const data = fs.readFileSync(ID_FILE, 'utf-8');
            const id = data.trim();
            if (id) return id;
        }
    } catch (e) {
        console.error("Error reading ID file:", e);
    }
    return null;
}

import pkg from 'whatsapp-web.js';
const { MessageMedia } = pkg;

app.post('/send', async (req, res) => {
    try {
        const { chatId, text, quotedMessageId, mediaPath } = req.body;
        // @ts-ignore
        const client = waManager.client;
        
        let options = {};
        if (quotedMessageId) {
            options = { quotedMessageId };
        }
        
        let contentToSend: any = text;
        if (mediaPath) {
            const media = MessageMedia.fromFilePath(mediaPath);
            contentToSend = media;
            if (text) {
                // @ts-ignore
                options.caption = text;
            }
        }
        
        await client.sendMessage(chatId, contentToSend, options);
        res.status(200).json({ success: true });
    } catch (err: any) {
        console.error("Error sending message:", err);
        res.status(500).json({ error: err.message });
    }
});

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const targetChatId = process.argv[2];
    
    if (!targetChatId) {
        console.error("Usage: node smart_monitor.js <chatId>");
        process.exit(1);
    }
    
    const checkInterval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(checkInterval);
            console.log(`Client is ready! Processing backlog for ${targetChatId}...`);
            
            try {
                // @ts-ignore
                const client = waManager.client;
                const chat = await client.getChatById(targetChatId);
                const lastMsgId = await getSavedMsgId();
                console.log(`Checking for messages after ID: ${lastMsgId}`);
                
                const messages = await chat.fetchMessages({ limit: 50 });
                let missedCount = 0;
                
                let startIndex = 0;
                if (lastMsgId) {
                    const lastMsgIndex = messages.findIndex((m: any) => m.id._serialized === lastMsgId);
                    if (lastMsgIndex !== -1) {
                        startIndex = lastMsgIndex + 1;
                    } else {
                        console.log(`Warning: Last known message ID (${lastMsgId}) not found in the last 50 messages. Processing all 50 as backlog.`);
                    }
                }
                
                for (let i = startIndex; i < messages.length; i++) {
                    const msg = messages[i];
                    missedCount++;
                    const sender = msg.author || msg.from;
                    console.log(`[BACKLOG] [${new Date(msg.timestamp * 1000).toLocaleString()}] ${sender} (ID: ${msg.id._serialized}): ${msg.body}`);
                }
                
                console.log(`Processed ${missedCount} missed messages.`);
                console.log("Starting live monitoring...");
                
                client.on('message_create', async (msg: any) => {
                    if (msg.from === targetChatId || msg.to === targetChatId) {
                        const sender = msg.author || msg.from;
                        console.log(`[LIVE] [${new Date(msg.timestamp * 1000).toLocaleString()}] ${sender} (ID: ${msg.id._serialized}): ${msg.body}`);
                    }
                });
                
                app.listen(3000, () => {
                    console.log('Local API Server listening on port 3000');
                });
                
            } catch (err) {
                console.error("Error during smart monitor execution:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
