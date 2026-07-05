import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Creating group...");
            
            try {
                // We use the underlying whatsapp-web.js client directly to call createGroup
                const client = waManager.client;
                
                // IDs to add
                const participants = [
                    "7426149486726@lid", // Salvatore Hanusiewicz
                    "266919366103131@lid"  // William Hanusiewicz
                ];
                
                const response = await client.createGroup("AI Chat Test", participants);
                console.log("Group created successfully!", response);
                process.exit(0);
            } catch (err) {
                console.error("Error creating group:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
