import { waManager } from "./whatsappClient.js";
import * as fs from 'fs';
import * as path from 'path';
import express from 'express';

const app = express();
app.use(express.json());

const ID_FILE = path.join(process.cwd(), 'last_processed_msg_id.txt');
const MEMORY_LOG_FILE = path.join(process.cwd(), 'chat_history.txt');
const TRIPWIRE_FILE = path.join(process.cwd(), 'tripwire.txt');

function appendToMemoryLog(logString: string) {
    try {
        fs.appendFileSync(MEMORY_LOG_FILE, logString + '\n');
    } catch (e) {
        console.error("Error writing to memory log:", e);
    }
}

function triggerTripwire() {
    try {
        fs.writeFileSync(TRIPWIRE_FILE, 'TRIGGERED');
    } catch (e) {
        console.error("Error writing to tripwire:", e);
    }
}

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

const contactCache = new Map<string, string>();
const messageBodyCache = new Map<string, string>();

function isBotTrigger(body: string): boolean {
    if (!body) return false;
    const lower = body.trim().toLowerCase();
    return lower.startsWith('agy') || lower.startsWith('@agy') || lower.startsWith('/');
}

import * as dotenv from 'dotenv';
dotenv.config();

const adminWhitelistRaw = process.env.ADMIN_WHITELIST || "";
const ADMIN_WHITELIST = adminWhitelistRaw.split(',').map(s => s.trim()).filter(s => s.length > 0);

function isAdmin(sender: string, contactName: string): boolean {
    if (ADMIN_WHITELIST.includes(contactName)) return true;
    
    let baseId = sender;
    if (sender.includes('@lid')) {
        baseId = sender.split('@')[0].split(':')[0];
    } else if (sender.includes(':')) {
        baseId = sender.split(':')[0];
    } else {
        baseId = sender.split('@')[0];
    }
    
    if (ADMIN_WHITELIST.includes(baseId)) return true;
    
    const lowerName = contactName.toLowerCase();
    for (const admin of ADMIN_WHITELIST) {
        if (lowerName.includes(admin.toLowerCase())) return true;
    }
    
    return false;
}

function cacheMessage(msgId: string, body: string) {
    if (!body) return;
    messageBodyCache.set(msgId, body);
    if (messageBodyCache.size > 50) {
        const firstKey = messageBodyCache.keys().next().value;
        if (firstKey) messageBodyCache.delete(firstKey);
    }
}

async function resolveContactName(client: any, msg: any, sender: string): Promise<string> {
    let baseId = sender;
    if (sender.includes('@lid')) {
        baseId = sender.split('@')[0].split(':')[0] + '@lid';
    } else if (sender.includes(':')) {
        baseId = sender.replace(/:\d+/, '');
    }

    if (contactCache.has(baseId)) {
        return contactCache.get(baseId)!;
    }

    let contactName = sender;
    try {
        let contact = await msg.getContact();
        if (!contact.name && !contact.pushname) {
            contact = await client.getContactById(baseId);
        }
        contactName = contact.name || contact.pushname || sender;

        if (contactName !== sender && contactName !== baseId) {
            contactCache.set(baseId, contactName);
        }
    } catch(e) {}
    
    return contactName;
}

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
                
                // Pre-warm the caches silently with the history
                for (let i = 0; i < messages.length; i++) {
                    const msg = messages[i];
                    const sender = msg.author || msg.from;
                    await resolveContactName(client, msg, sender);
                    cacheMessage(msg.id._serialized, msg.body);
                }
                
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
                    const contactName = await resolveContactName(client, msg, sender);
                    cacheMessage(msg.id._serialized, msg.body);
                    const logStr = `[BACKLOG] [${new Date(msg.timestamp * 1000).toLocaleString()}] ${contactName} (ID: ${sender}) (MsgID: ${msg.id._serialized}): ${msg.body}`;
                    appendToMemoryLog(logStr);
                    if (isBotTrigger(msg.body) && isAdmin(sender, contactName)) {
                        console.log(logStr);
                        triggerTripwire();
                    }
                }
                
                console.log(`Processed ${missedCount} missed messages.`);
                console.log("Starting live monitoring...");
                
                client.on('message_create', async (msg: any) => {
                    if (msg.from === targetChatId || msg.to === targetChatId) {
                        const sender = msg.author || msg.from;
                        const contactName = await resolveContactName(client, msg, sender);
                        cacheMessage(msg.id._serialized, msg.body);
                        const logStr = `[LIVE] [${new Date(msg.timestamp * 1000).toLocaleString()}] ${contactName} (ID: ${sender}) (MsgID: ${msg.id._serialized}): ${msg.body}`;
                        appendToMemoryLog(logStr);
                        if (isBotTrigger(msg.body) && isAdmin(sender, contactName)) {
                            console.log(logStr);
                            triggerTripwire();
                        }
                    }
                });
                
                client.on('message_edit', async (msg: any, newBody: string, prevBody: string) => {
                    if (msg.from === targetChatId || msg.to === targetChatId) {
                        const sender = msg.author || msg.from;
                        const contactName = await resolveContactName(client, msg, sender);
                        cacheMessage(msg.id._serialized, newBody);
                        const logStr = `[EDIT] [${new Date(msg.timestamp * 1000).toLocaleString()}] ${contactName} (ID: ${sender}) (MsgID: ${msg.id._serialized}): changed "${prevBody}" to "${newBody}"`;
                        appendToMemoryLog(logStr);
                        if ((isBotTrigger(prevBody) || isBotTrigger(newBody)) && isAdmin(sender, contactName)) {
                            console.log(logStr);
                            triggerTripwire();
                        }
                    }
                });
                
                client.on('message_revoke_everyone', async (after: any, before: any) => {
                    const revokedMsgId = after?.id?._serialized || before?.id?._serialized;
                    const sender = after?.author || after?.from || before?.author || before?.from;
                    
                    if (!revokedMsgId || !sender) return;
                    
                    const from = after?.from || before?.from;
                    const to = after?.to || before?.to;
                    if (from !== targetChatId && to !== targetChatId) return;

                    const originalBody = messageBodyCache.get(revokedMsgId) || before?.body || "";
                    const contactName = await resolveContactName(client, after || before, sender);
                    
                    const logStr = `[DELETED] [${new Date().toLocaleString()}] ${contactName} (ID: ${sender}) (MsgID: ${revokedMsgId}): deleted "${originalBody}"`;
                    appendToMemoryLog(logStr);
                    if (isBotTrigger(originalBody) && isAdmin(sender, contactName)) {
                        console.log(logStr);
                        triggerTripwire();
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
