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
        let target = pages.find(p => p.url().includes('modstore/scorm'));
        if(!target) {
            console.log("No scorm found.");
            return process.exit(1);
        }
        
        let html = await target.evaluate(() => {
            return document.body.innerHTML;
        });
        require('fs').writeFileSync('scorm_html.txt', html);
        console.log("Dumped html");
        
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
