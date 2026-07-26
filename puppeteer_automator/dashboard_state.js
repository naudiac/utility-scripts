const puppeteer = require('puppeteer-core');
const axios = require('axios');
const fs = require('fs');

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
        await new Promise(r => setTimeout(r, 2000));
        await target.screenshot({path: 'C:\\Users\\whanusiewicz\\puppeteer_agent\\dashboard_current.png'});
        
        let allText = await target.evaluate(() => document.body ? document.body.innerText : '');
        let clickableElements = await target.evaluate(() => {
            const nodes = Array.from(document.querySelectorAll('button, a, [role="button"]'));
            return nodes.map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    text: el.innerText ? el.innerText.trim().replace(/\n/g, ' ') : '',
                    className: el.className,
                    href: el.href || '',
                    rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height }
                };
            }).filter(e => e.text && e.rect.width > 0 && e.rect.height > 0);
        });

        fs.writeFileSync('C:\\Users\\whanusiewicz\\puppeteer_agent\\dashboard_ui_state.json', JSON.stringify({text: allText, elements: clickableElements}, null, 2));
        console.log("Dashboard state extracted.");
        
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
