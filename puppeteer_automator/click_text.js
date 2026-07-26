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
        
        const targetText = process.argv[2];
        let clicked = false;
        
        const frames = target.frames();
        for(let frame of frames) {
            try {
                const didClick = await frame.evaluate((textToFind) => {
                    let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    while (node = walker.nextNode()) {
                        if (node.nodeValue.includes(textToFind)) {
                            let el = node.parentElement;
                            while(el && el.tagName !== 'BUTTON' && el.tagName !== 'A' && el.tagName !== 'LABEL' && el.tagName !== 'LI') {
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
        else {
            console.log("Waiting 1s...");
            await new Promise(r => setTimeout(r, 1000));
            await target.screenshot({path: 'C:\\Users\\whanusiewicz\\puppeteer_agent\\after.png'});
        }
        await browser.disconnect();
    } catch(e) {
        console.log(e);
    }
})();
