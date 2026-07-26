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
        let target = pages.find(p => p.url().includes('modstore') || p.url().includes('scorm'));
        if(!target) {
            console.log("No course popup found.");
            return process.exit(1);
        }
        
        const selector = process.argv[2] || "button";
        let clicked = false;
        
        const frames = target.frames();
        for(let frame of frames) {
            try {
                const didClick = await frame.evaluate((sel) => {
                    let el = document.querySelector(sel);
                    if(el) {
                        const rect = el.getBoundingClientRect();
                        if(rect.top >= 0 && rect.width > 0) {
                            el.click();
                            return true;
                        }
                    }
                    return false;
                }, selector);
                if(didClick) {
                    console.log("Clicked successfully:", selector);
                    clicked = true;
                    break;
                }
            } catch(e) {}
        }
        
        if(!clicked) console.log("Failed to click:", selector);
        else {
            console.log("Waiting 3s...");
            await new Promise(r => setTimeout(r, 3000));
            await target.screenshot({path: 'C:\\Users\\whanusiewicz\\puppeteer_agent\\after.png'});
            console.log("Screenshot saved.");
        }
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
