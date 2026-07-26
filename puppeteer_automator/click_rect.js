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
        let x = parseFloat(process.argv[2]);
        let y = parseFloat(process.argv[3]);
        
        console.log("Clicking at", x, y);
        await target.mouse.click(x, y);
        console.log("Clicked successfully.");
        
        await new Promise(r => setTimeout(r, 3000));
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
