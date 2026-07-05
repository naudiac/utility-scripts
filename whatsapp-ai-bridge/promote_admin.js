import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Promoting Sal to admin...");
            
            try {
                const client = waManager.client;
                const groupId = "120363427507526294@g.us";
                const chat = await client.getChatById(groupId);
                
                if (chat.isGroup) {
                    const participantsToPromote = chat.participants
                        .filter(p => !p.isAdmin && !p.isSuperAdmin)
                        .map(p => p.id._serialized);
                    
                    if (participantsToPromote.length > 0) {
                        await chat.promoteParticipants(participantsToPromote);
                        console.log("Successfully promoted Sal to admin!");
                    } else {
                        console.log("Everyone is already an admin!");
                    }
                } else {
                    console.error("Chat is not a group!");
                }
                process.exit(0);
            } catch (err) {
                console.error("Error promoting:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
