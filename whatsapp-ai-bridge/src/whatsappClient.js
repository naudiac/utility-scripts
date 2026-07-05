"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.waManager = exports.WhatsAppManager = void 0;
const whatsapp_web_js_1 = require("whatsapp-web.js");
const qrcode = __importStar(require("qrcode-terminal"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
class WhatsAppManager {
    client;
    isReady = false;
    currentQr = null;
    initPromise = null;
    constructor() {
        this.client = new whatsapp_web_js_1.Client({
            authStrategy: new whatsapp_web_js_1.LocalAuth({ dataPath: './whatsapp_auth' }),
            puppeteer: {
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        });
        this.client.on('qr', (qr) => {
            this.currentQr = qr;
            console.error('[WhatsApp] QR code generated. Please scan it.');
            qrcode.generate(qr, { small: true });
        });
        this.client.on('ready', () => {
            this.isReady = true;
            this.currentQr = null;
            console.error('[WhatsApp] Client is ready!');
        });
        this.client.on('authenticated', () => {
            console.error('[WhatsApp] Client authenticated!');
        });
        this.client.on('auth_failure', msg => {
            console.error('[WhatsApp] Auth failure', msg);
        });
    }
    async initialize() {
        if (!this.initPromise) {
            this.initPromise = this.client.initialize();
        }
        return this.initPromise;
    }
    getQrCode() {
        return this.currentQr;
    }
    getStatus() {
        return this.isReady ? 'ready' : (this.currentQr ? 'waiting_for_qr_scan' : 'initializing');
    }
    async sendMessage(to, body, mediaPath) {
        if (!to.includes('@')) {
            to = `${to}@c.us`; // Default to individual chat
        }
        let media;
        if (mediaPath) {
            if (!fs.existsSync(mediaPath)) {
                throw new Error(`Media file not found at path: ${mediaPath}`);
            }
            media = whatsapp_web_js_1.MessageMedia.fromFilePath(mediaPath);
        }
        return await this.client.sendMessage(to, body, { media });
    }
    async readMessages(chatId, limit = 10) {
        if (!chatId.includes('@')) {
            chatId = `${chatId}@c.us`;
        }
        const chat = await this.client.getChatById(chatId);
        return await chat.fetchMessages({ limit });
    }
    async searchChats(query, limit = 20) {
        return await this.client.searchMessages(query, { limit });
    }
    async getChats() {
        return await this.client.getChats();
    }
}
exports.WhatsAppManager = WhatsAppManager;
exports.waManager = new WhatsAppManager();
//# sourceMappingURL=whatsappClient.js.map