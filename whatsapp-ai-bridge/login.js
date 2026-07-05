import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    // We just wait here indefinitely.
    // If auth succeeds, or if QR is generated, it will print to console.
    // The agent can observe the console output.
    setInterval(() => {
        if (waManager.getStatus() === 'ready') {
            console.log("Client is fully authenticated and ready!");
            process.exit(0);
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
