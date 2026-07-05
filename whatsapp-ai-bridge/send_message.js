import { waManager } from "./dist/whatsappClient.js";
import pkg from "whatsapp-web.js";
const { MessageMedia } = pkg;

async function run() {
    const targetChatId = process.argv[2];
    const message = process.argv[3];
    const quotedMessageId = process.argv[4];
    const mediaPath = process.argv[5];
    
    if (!targetChatId || !message) {
        console.error("Usage: node send_message.js <chatId> <message> [quotedMessageId] [mediaPath]");
        process.exit(1);
    }
    
    try {
        const payload = { chatId: targetChatId, text: message, quotedMessageId, mediaPath };
        const response = await fetch('http://localhost:3000/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            console.log("Successfully sent message via local API!");
            process.exit(0);
        }
    } catch (e) {
        // API server not running, fallback to booting client
    }

    console.log("Initializing WhatsApp Client (Fallback)...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log(`Client is ready! Sending message to ${targetChatId}...`);
            
            try {
                const client = waManager.client;
                let options = {};
                if (quotedMessageId) {
                    // @ts-ignore
                    options.quotedMessageId = quotedMessageId;
                }
                
                let contentToSend = message;
                if (mediaPath) {
                    const media = MessageMedia.fromFilePath(mediaPath);
                    contentToSend = media;
                    // @ts-ignore
                    options.caption = message;
                }
                
                await client.sendMessage(targetChatId, contentToSend, options);
                console.log("Successfully sent message!");
                process.exit(0);
            } catch (err) {
                console.error("Error sending:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
