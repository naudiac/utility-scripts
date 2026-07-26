const puppeteer = require('puppeteer-core');
const axios = require('axios');

(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:9222/json/version');
        const browser = await puppeteer.connect({
            browserWSEndpoint: response.data.webSocketDebuggerUrl,
            defaultViewport: null
        });
        const pages = await browser.pages();
        let target = pages.find(p => p.url().includes('lx/training'));
        if(!target) {
            console.log("No dashboard found.");
            return process.exit(1);
        }
        
        await target.bringToFront();
        await target.reload({ waitUntil: 'networkidle2' });
        console.log("Reloaded dashboard");
        
        const rect = await target.evaluate(() => {
            let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let node;
            while (node = walker.nextNode()) {
                if (node.nodeValue.trim() === 'Start' || node.nodeValue.trim() === 'Resume') {
                    let el = node.parentElement;
                    while(el && el.tagName !== 'BUTTON' && el.tagName !== 'A') {
                        if(el.tagName === 'BODY') break;
                        el = el.parentElement;
                    }
                    if(el && el.tagName !== 'BODY') {
                        let r = el.getBoundingClientRect();
                        return { text: node.nodeValue.trim(), x: r.left + r.width/2, y: r.top + r.height/2 };
                    }
                }
            }
            return null;
        });
        
        if(rect) {
            console.log("Clicking", rect.text, "at", rect.x, rect.y);
            await target.mouse.click(rect.x, rect.y);
            console.log("Clicked trusted successfully.");
        } else {
            console.log("Failed to find Start or Resume.");
        }
        
        await new Promise(r => setTimeout(r, 3000));
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
