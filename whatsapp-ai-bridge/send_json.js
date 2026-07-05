import { waManager } from "./dist/whatsappClient.js";
import pkg from 'whatsapp-web.js';
const { MessageMedia } = pkg;

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Sending JSON document...");
            
            try {
                const client = waManager.client;
                const groupId = "120363427507526294@g.us";
                const filePath = "C:\\Users\\whanusiewicz\\.gemini\\antigravity\\scratch\\whatsapp-mcp\\whatsapp_mcp_handover.json";
                
                const media = MessageMedia.fromFilePath(filePath);
                
                await client.sendMessage(groupId, media, { caption: "Here is the architectural JSON handover for Sal's AGY!" });
                
                console.log("Successfully sent the JSON document!");
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
