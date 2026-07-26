const puppeteer = require('puppeteer-core');
const axios = require('axios');
(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:9222/json/version');
        const browser = await puppeteer.connect({ browserWSEndpoint: response.data.webSocketDebuggerUrl, defaultViewport: null });
        const pages = await browser.pages();
        for(let p of pages) {
            console.log(p.url());
        }
        await browser.disconnect();
    } catch(e) { console.log(e); }
})();
