import pkg from 'whatsapp-web.js';
const { Client, LocalAuth, MessageMedia } = pkg;
import * as qrcode from 'qrcode-terminal';
import QRCode from 'qrcode';
import * as path from 'path';
import * as fs from 'fs';

export class WhatsAppManager {
    private client: any; // using any to avoid type issues with pkg
    private isReady: boolean = false;
    private currentQr: string | null = null;
    private initPromise: Promise<void> | null = null;

    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth({ dataPath: './whatsapp_auth' }),
            puppeteer: {
                executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        });

        this.client.on('qr', async (qr: string) => {
            this.currentQr = qr;
            console.error('[WhatsApp] QR code generated. Please scan it.');
            const qrPath = path.join(process.cwd(), 'whatsapp_qr.png');
            await QRCode.toFile(qrPath, qr);
            console.log(`\nQR Code generated and saved to: ${qrPath}`);
            // qrcode.generate(qr, { small: true });
        });

        this.client.on('ready', () => {
            this.isReady = true;
            this.currentQr = null;
            console.error('[WhatsApp] Client is ready!');
        });

        this.client.on('authenticated', () => {
            console.error('[WhatsApp] Client authenticated!');
        });

        this.client.on('auth_failure', (msg: any) => {
            console.error('[WhatsApp] Auth failure', msg);
        });
    }

    public async initialize() {
        if (!this.initPromise) {
            this.initPromise = this.client.initialize();
        }
        return this.initPromise;
    }

    public getQrCode(): string | null {
        return this.currentQr;
    }

    public getStatus(): string {
        return this.isReady ? 'ready' : (this.currentQr ? 'waiting_for_qr_scan' : 'initializing');
    }

    public async sendMessage(to: string, body: string, mediaPath?: string) {
        if (!to.includes('@')) {
            to = `${to}@c.us`; // Default to individual chat
        }
        
        let media: any;
        if (mediaPath) {
            if (!fs.existsSync(mediaPath)) {
                throw new Error(`Media file not found at path: ${mediaPath}`);
            }
            media = MessageMedia.fromFilePath(mediaPath);
        }
        
        return await this.client.sendMessage(to, body, { media });
    }

    public async readMessages(chatId: string, limit: number = 10): Promise<any[]> {
        if (!chatId.includes('@')) {
            chatId = `${chatId}@c.us`;
        }
        const chat = await this.client.getChatById(chatId);
        return await chat.fetchMessages({ limit });
    }

    public async searchChats(query: string, limit: number = 20): Promise<any[]> {
        return await this.client.searchMessages(query, { limit });
    }

    public async getChats(): Promise<any[]> {
        return await this.client.getChats();
    }
}

export const waManager = new WhatsAppManager();
