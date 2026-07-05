import { Message, Chat } from 'whatsapp-web.js';
export declare class WhatsAppManager {
    private client;
    private isReady;
    private currentQr;
    private initPromise;
    constructor();
    initialize(): Promise<void>;
    getQrCode(): string | null;
    getStatus(): string;
    sendMessage(to: string, body: string, mediaPath?: string): Promise<Message>;
    readMessages(chatId: string, limit?: number): Promise<Message[]>;
    searchChats(query: string, limit?: number): Promise<Message[]>;
    getChats(): Promise<Chat[]>;
}
export declare const waManager: WhatsAppManager;
//# sourceMappingURL=whatsappClient.d.ts.map