import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Setting description...");
            
            try {
                const client = waManager.client;
                
                // Get the Group Chat by ID
                const groupId = "120363427507526294@g.us";
                const chat = await client.getChatById(groupId);
                
                if (chat.isGroup) {
                    await chat.setDescription("Testing WhatsApp MCP capabilities.");
                    console.log("Group description updated successfully!");
                } else {
                    console.error("Chat is not a group!");
                }
                process.exit(0);
            } catch (err) {
                console.error("Error setting description:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
