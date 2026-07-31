import * as fs from 'fs';
import * as path from 'path';

const ID_FILE = path.join(process.cwd(), 'last_processed_msg_id.txt');

const msgId = process.argv[2];

if (!msgId) {
    console.error("Usage: node update_last_msg.js <msg_id._serialized>");
    process.exit(1);
}

fs.writeFileSync(ID_FILE, msgId, 'utf-8');
console.log(`Updated last processed message ID to: ${msgId}`);
