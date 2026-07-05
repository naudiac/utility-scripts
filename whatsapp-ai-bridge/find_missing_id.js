import { waManager } from "./dist/whatsappClient.js";

async function run() {
    await waManager.initialize();
    
    const interval = setInterval(async () => {
        if (waManager.getStatus() === 'ready') {
            clearInterval(interval);
            try {
                const client = waManager.client;
                const chat = await client.getChatById("120363427507526294@g.us");
                const messages = await chat.fetchMessages({ limit: 5 });
                for (const msg of messages) {
                    if (msg.body && msg.body.includes("also update it on")) {
                        console.log("FOUND MESSAGE ID:", msg.id._serialized);
                    }
                }
                process.exit(0);
            } catch (err) {
                console.error("Error:", err);
                process.exit(1);
            }
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
