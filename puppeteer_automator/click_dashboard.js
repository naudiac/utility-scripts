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
        
        const targetText = process.argv[2];
        let clicked = false;
        
        const frames = target.frames();
        for(let frame of frames) {
            try {
                const didClick = await frame.evaluate((textToFind) => {
                    let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    while (node = walker.nextNode()) {
                        if (node.nodeValue.trim() === textToFind) {
                            let el = node.parentElement;
                            while(el && el.tagName !== 'BUTTON' && el.tagName !== 'A') {
                                if(el.tagName === 'BODY') break;
                                el = el.parentElement;
                            }
                            if(el && el.tagName !== 'BODY') {
                                el.click();
                                return true;
                            } else {
                                node.parentElement.click();
                                return true;
                            }
                        }
                    }
                    return false;
                }, targetText);
                if(didClick) {
                    console.log("Clicked text successfully:", targetText);
                    clicked = true;
                    break;
                }
            } catch(e) {}
        }
        
        if(!clicked) console.log("Failed to click text:", targetText);
        
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
