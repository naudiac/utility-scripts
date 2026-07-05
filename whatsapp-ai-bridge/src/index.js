"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const whatsappClient_js_1 = require("./whatsappClient.js");
const server = new mcp_js_1.McpServer({
    name: "whatsapp-mcp",
    version: "1.0.0"
});
// Register tools
server.tool("get_qr_code", "Get the current WhatsApp authentication QR code string. Useful for displaying the QR to the user so they can scan it.", {}, async () => {
    const status = whatsappClient_js_1.waManager.getStatus();
    const qr = whatsappClient_js_1.waManager.getQrCode();
    if (status === 'ready') {
        return {
            content: [{ type: "text", text: "WhatsApp is already authenticated and ready." }]
        };
    }
    if (qr) {
        return {
            content: [{ type: "text", text: `Scan this QR Code:\n\n${qr}\n\nYou can render this using a QR generator tool or library.` }]
        };
    }
    return {
        content: [{ type: "text", text: `WhatsApp status is: ${status}. No QR code available yet.` }]
    };
});
server.tool("send_message", "Send a text message to a WhatsApp number. The 'to' parameter should be the phone number (with country code, e.g., 15551234567).", {
    to: zod_1.z.string().describe("Phone number with country code (no + or spaces) or chat ID."),
    body: zod_1.z.string().describe("The message text to send."),
    mediaPath: zod_1.z.string().optional().describe("Optional absolute path to a local media file (image/document) to attach.")
}, async ({ to, body, mediaPath }) => {
    if (whatsappClient_js_1.waManager.getStatus() !== 'ready') {
        return { content: [{ type: "text", text: "WhatsApp client is not ready. Please authenticate first." }] };
    }
    try {
        await whatsappClient_js_1.waManager.sendMessage(to, body, mediaPath);
        return { content: [{ type: "text", text: `Message sent successfully to ${to}.` }] };
    }
    catch (error) {
        return { content: [{ type: "text", text: `Failed to send message: ${error.message}` }], isError: true };
    }
});
server.tool("read_messages", "Read the most recent messages from a specific chat.", {
    chatId: zod_1.z.string().describe("Phone number or chat ID to read from."),
    limit: zod_1.z.number().optional().default(10).describe("Number of messages to retrieve.")
}, async ({ chatId, limit }) => {
    if (whatsappClient_js_1.waManager.getStatus() !== 'ready') {
        return { content: [{ type: "text", text: "WhatsApp client is not ready." }] };
    }
    try {
        const msgs = await whatsappClient_js_1.waManager.readMessages(chatId, limit);
        const formatted = msgs.map(m => `[${new Date(m.timestamp * 1000).toISOString()}] ${m.fromMe ? 'Me' : m.from}: ${m.body}${m.hasMedia ? ' [Media Attached]' : ''}`).join('\n');
        return { content: [{ type: "text", text: formatted || "No messages found." }] };
    }
    catch (error) {
        return { content: [{ type: "text", text: `Failed to read messages: ${error.message}` }], isError: true };
    }
});
server.tool("search_chats", "Search all chat history for a specific keyword.", {
    query: zod_1.z.string().describe("Keyword to search for."),
    limit: zod_1.z.number().optional().default(20).describe("Max results to return.")
}, async ({ query, limit }) => {
    if (whatsappClient_js_1.waManager.getStatus() !== 'ready') {
        return { content: [{ type: "text", text: "WhatsApp client is not ready." }] };
    }
    try {
        const msgs = await whatsappClient_js_1.waManager.searchChats(query, limit);
        const formatted = msgs.map(m => `[${new Date(m.timestamp * 1000).toISOString()}] Chat: ${m.from} - ${m.body}`).join('\n');
        return { content: [{ type: "text", text: formatted || "No results found." }] };
    }
    catch (error) {
        return { content: [{ type: "text", text: `Failed to search chats: ${error.message}` }], isError: true };
    }
});
async function main() {
    console.error("Initializing WhatsApp Manager...");
    whatsappClient_js_1.waManager.initialize().catch(console.error);
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
    console.error("WhatsApp MCP Server running on stdio");
}
main().catch(console.error);
//# sourceMappingURL=index.js.map