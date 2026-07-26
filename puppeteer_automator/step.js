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
        let target = pages.find(p => p.url().includes('modstore') || p.url().includes('scorm'));
        
        if (!target) {
            console.log("Could not find relevant page.");
            await browser.disconnect();
            return;
        }

        await target.bringToFront();
        await new Promise(r => setTimeout(r, 1000));
        
        await target.screenshot({path: 'C:\\Users\\whanusiewicz\\puppeteer_agent\\before.png'});
        
        let clickableElements = [];
        let allText = [];
        const frames = target.frames();
        for (let i = 0; i < frames.length; i++) {
            let frame = frames[i];
            try {
                const text = await frame.evaluate(() => document.body ? document.body.innerText : '');
                if (text && text.trim()) allText.push(`--- Frame ${i} ---\n${text.trim()}`);
                
                const els = await frame.evaluate(() => {
                    const nodes = Array.from(document.querySelectorAll('button, a, [role="button"], .next-btn, .play-btn, [class*="answer"], [class*="choice"]'));
                    return nodes.map(el => {
                        const rect = el.getBoundingClientRect();
                        return {
                            tag: el.tagName,
                            text: el.innerText ? el.innerText.trim().replace(/\n/g, ' ') : '',
                            className: el.className,
                            id: el.id,
                            rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height }
                        };
                    }).filter(e => e.text && e.rect.width > 0 && e.rect.height > 0);
                });
                if (els.length > 0) {
                    clickableElements.push({ frameIndex: i, frameUrl: frame.url(), elements: els });
                }
            } catch (err) { }
        }
        
        console.log("Extracted UI state.");
        fs.writeFileSync('C:\\Users\\whanusiewicz\\puppeteer_agent\\ui_state.json', JSON.stringify({text: allText, elements: clickableElements}, null, 2));
        
        await browser.disconnect();
    } catch (e) {
        console.error("Error:", e.message);
    }
})();
