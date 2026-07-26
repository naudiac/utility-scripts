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
        
        await target.bringToFront();
        
        await target.evaluate(() => {
            let selects = document.querySelectorAll('select');
            selects.forEach(s => {
                let options = Array.from(s.options);
                let alwaysOpt = options.find(o => o.text.trim() === 'Always');
                if(alwaysOpt) {
                    s.value = alwaysOpt.value;
                } else {
                    s.selectedIndex = 1; // Try setting it to first real option
                }
                s.dispatchEvent(new Event('change', {bubbles: true}));
            });
            
            // If they are custom dropdowns
            let elems = document.querySelectorAll('select');
            if (elems.length === 0) {
               console.log("No selects found, attempting custom dropdowns.");
            }
        });
        
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
