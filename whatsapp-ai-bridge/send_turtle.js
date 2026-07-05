import { waManager } from "./dist/whatsappClient.js";
import pkg from 'whatsapp-web.js';
const { MessageMedia } = pkg;

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            console.log("Client is ready! Sending image...");
            
            try {
                const client = waManager.client;
                const groupId = "120363427507526294@g.us";
                const imagePath = "C:\\Users\\whanusiewicz\\.gemini\\antigravity\\brain\\2f739d6f-9309-4551-b68c-8eb54e1ea98f\\turtle_1783251320249.png";
                
                const media = MessageMedia.fromFilePath(imagePath);
                
                await client.sendMessage(groupId, media, { caption: "Here is your turtle! 🐢" });
                
                console.log("Successfully sent the turtle!");
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
