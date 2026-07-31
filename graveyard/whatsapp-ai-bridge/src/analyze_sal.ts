import { waManager } from "./whatsappClient.js";

async function analyze() {
    console.log("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    await new Promise(resolve => (waManager as any).client.on('ready', resolve));
    console.log("Client initialized and READY! Fetching all chats...");
    const chats = await (waManager as any).client.getChats();
    
    console.log(`Found ${chats.length} total chats. Looking for Sal...`);
    
    // Look for chats with Sal
    const salChats = chats.filter((chat: any) => {
        return chat.name.toLowerCase().includes('sal') || chat.name.toLowerCase().includes('ai chat test') || chat.isGroup; 
    });
    
    console.log(`Analyzing ${salChats.length} potential chats for Sal's sword requests...`);
    
    const threeDaysAgo = Math.floor(Date.now() / 1000) - (3 * 24 * 60 * 60);
    const results: {ts: number, text: string}[] = [];

    for (const chat of salChats) {
        try {
            const messages = await chat.fetchMessages({ limit: 1000 });
            for (const msg of messages) {
                if (msg.timestamp >= threeDaysAgo) {
                    const sender = msg.author || msg.from;
                    const body = msg.body.toLowerCase();
                    // Just log all recent messages that contain 'sword' or from Sal
                    if (body.includes('sword') || body.includes('sal') || body.includes('agy')) {
                        const contact = await (waManager as any).client.getContactById(sender);
                        const senderName = contact.pushname || contact.name || sender;
                        results.push({
                            ts: msg.timestamp,
                            text: `[${new Date(msg.timestamp * 1000).toLocaleString()}] ${senderName} in ${chat.name}: ${msg.body}`
                        });
                    }
                }
            }
        } catch (e) {
            console.error(`Error fetching messages for ${chat.name}:`, e);
        }
    }
    
    console.log("\n--- SWORD-RELATED CHAT HISTORY (Last 3 Days) ---");
    results.sort((a, b) => a.ts - b.ts);
    for (const r of results) {
        console.log(r.text);
    }
    
    process.exit(0);
}

analyze().catch(console.error);
