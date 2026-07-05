import { waManager } from "./dist/whatsappClient.js";
import QRCode from "qrcode";
import fs from "fs";

async function run() {
    console.log("Starting WhatsApp client...");
    await waManager.initialize();
    
    let lastQr = null;

    // Wait until we get a QR code or are ready
    const interval = setInterval(async () => {
        const qr = waManager.getQrCode();
        if (qr && qr !== lastQr) {
            lastQr = qr;
            console.log("Got new QR Code string. Updating image...");
            const outPath = "C:\\Users\\whanusiewicz\\.gemini\\antigravity\\brain\\2f739d6f-9309-4551-b68c-8eb54e1ea98f\\whatsapp_qr.png";
            await QRCode.toFile(outPath, qr);
            console.log("Saved updated QR code to:", outPath);
        }
        if (waManager.getStatus() === 'ready') {
            console.log("Authenticated successfully!");
            clearInterval(interval);
            process.exit(0);
        }
    }, 2000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
