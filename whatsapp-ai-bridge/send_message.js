import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const targetChatId = process.argv[2];
    const message = process.argv[3];
    const quotedMessageId = process.argv[4];
    
    if (!targetChatId || !message) {
        console.error("Usage: node send_message.js <chatId> <message> [quotedMessageId]");
        process.exit(1);
    }
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log(`Client is ready! Sending message to ${targetChatId}...`);
            
            try {
                const client = waManager.client;
                let options = {};
                if (quotedMessageId) {
                    options.quotedMessageId = quotedMessageId;
                }
                await client.sendMessage(targetChatId, message, options);
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
