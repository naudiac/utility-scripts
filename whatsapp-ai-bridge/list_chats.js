import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    // Wait for it to be ready
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Fetching recent chats...");
            
            try {
                const chats = await waManager.getChats();
                
                // Print top 10 recent chats
                console.log("\n--- Top 10 Recent Chats ---");
                const topChats = chats.slice(0, 10);
                for (let i = 0; i < topChats.length; i++) {
                    const chat = topChats[i];
                    console.log(`${i + 1}. ${chat.name || chat.id.user} (ID: ${chat.id._serialized}) - isGroup: ${chat.isGroup} - unread: ${chat.unreadCount}`);
                }
                console.log("---------------------------\n");
                process.exit(0);
            } catch (err) {
                console.error("Error fetching chats:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
