import { waManager } from "./whatsappClient.js";

async function run() {
    const targetChatId = process.argv[2]; // Optional filter
    
    console.error("Initializing WhatsApp Client...");
    await waManager.initialize();
    
    // We only attach the listener once the client is ready
    let listenerAttached = false;

    const interval = setInterval(() => {
        if (waManager.getStatus() === 'ready' && !listenerAttached) {
            listenerAttached = true;
            console.error(`Client is ready! Listening for next message${targetChatId ? ` in chat ${targetChatId}` : ''}...`);
            
            (waManager as any).client.on('message_create', async (msg: any) => {
                // If a targetChatId is provided, ignore messages from other chats
                if (targetChatId && msg.from !== targetChatId && msg.to !== targetChatId) {
                    return;
                }
                
                const chat = await msg.getChat();
                let contact = { name: "Me", pushname: "Me", number: msg.author || msg.from };
                try {
                    contact = await msg.getContact();
                } catch (err) {
                    console.error("Warning: Failed to get contact details (likely self-sent message).");
                }
                
                const output = {
                    chatName: chat.name || "Unknown",
                    chatId: chat.id._serialized,
                    messageId: msg.id._serialized,
                    senderName: contact.name || contact.pushname || contact.number,
                    senderId: msg.author || msg.from,
                    body: msg.body,
                    timestamp: msg.timestamp
                };
                
                // Print the message data as standard output
                console.log(JSON.stringify(output, null, 2));
                
                // Exit immediately to wake up the monitoring agent
                process.exit(0);
            });
        }
    }, 1000);
}

run().catch(e => {
    console.error("Error:", e);
    process.exit(1);
});
