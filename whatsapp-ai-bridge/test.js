import { waManager } from "./dist/whatsappClient.js";

async function run() {
    console.log("Starting WhatsApp client...");
    await waManager.initialize();
    
    // Wait until we get a QR code or are ready
    setInterval(() => {
        const qr = waManager.getQrCode();
        if (qr) {
            console.log("SUCCESS! Got QR Code string:");
            console.log(qr);
            process.exit(0);
        }
        if (waManager.getStatus() === 'ready') {
            console.log("Already authenticated!");
            process.exit(0);
        }
    }, 2000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
