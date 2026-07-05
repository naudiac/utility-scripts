import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const targetChatId = process.argv[2];
    const limit = parseInt(process.argv[3]) || 10;
    
    if (!targetChatId) {
        console.error("Usage: node read_messages.js <chatId> [limit]");
        process.exit(1);
    }
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log(`Client is ready! Fetching up to ${limit} messages from ${targetChatId}...`);
            
            try {
                const client = waManager.client;
                const chat = await client.getChatById(targetChatId);
                const messages = await chat.fetchMessages({ limit });
                
                console.log("\n--- MESSAGES ---");
                for (const msg of messages) {
                    const sender = msg.author || msg.from;
                    console.log(`[${new Date(msg.timestamp * 1000).toLocaleString()}] ${sender}: ${msg.body}`);
                }
                console.log("----------------\n");
                
                process.exit(0);
            } catch (err) {
                console.error("Error fetching messages:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
