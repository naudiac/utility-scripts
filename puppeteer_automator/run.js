const puppeteer = require('puppeteer-core');
const axios = require('axios');

const delay = ms => new Promise(res => setTimeout(res, ms));

(async () => {
    try {
        console.log("Fetching WebSocket endpoint...");
        const response = await axios.get('http://127.0.0.1:9222/json/version');
        const webSocketDebuggerUrl = response.data.webSocketDebuggerUrl;
        
        console.log("Connecting to Edge...");
        const browser = await puppeteer.connect({
            browserWSEndpoint: webSocketDebuggerUrl,
            defaultViewport: null
        });

        const pages = await browser.pages();
        
        // 1. Check if course popup is already open
        let activePage = pages.find(p => p.url().includes('modstore') || p.url().includes('scorm'));
        let dashboard = pages.find(p => p.url().includes('lx/training'));

        if (!activePage) {
            if (!dashboard) {
                console.log("Could not find the 'lx/training' dashboard page or course player.");
                await browser.disconnect();
                return;
            }
            console.log("Course popup not found, attempting to start from dashboard...");
            await dashboard.bringToFront();
            
            const buttons = await dashboard.$$('button, a');
            let clicked = false;
            for (let btn of buttons) {
                const text = await dashboard.evaluate(el => el.innerText, btn);
                if (text && (text.includes('Start') || text.includes('Resume'))) {
                    console.log(`Starting course... Clicking button: "${text.trim()}"`);
                    await btn.click();
                    clicked = true;
                    break;
                }
            }

            if (!clicked) {
                console.log("No Start or Resume buttons found on the dashboard. Is the training already complete?");
                await browser.disconnect();
                return;
            }
            console.log("Clicked! Waiting 5 seconds for the course player popup to load...");
            await delay(5000);
        } else {
            console.log("Course popup is already open!");
            await activePage.bringToFront();
        }

        console.log("Initiating background automation loop for the course popup...");
        
        let iteration = 0;
        while(iteration < 200) {
            iteration++;
            const currentPages = await browser.pages();
            
            // Re-find the active course popup in case it changed tabs
            let popup = currentPages.find(p => p.url().includes('modstore') || p.url().includes('scorm'));
            
            // Only scan the popup if it exists. If not, fallback to all (in case URL structure changed).
            let pagesToScan = popup ? [popup] : currentPages;

            for (let p of pagesToScan) {
                try {
                    const frames = p.frames();
                    for (let frame of frames) {
                        try {
                            const didClick = await frame.evaluate(() => {
                                let btns = Array.from(document.querySelectorAll('button, a, .next-btn, .play-btn')).filter(el => {
                                    if(!el.innerText) return false;
                                    let t = el.innerText.toLowerCase().trim();
                                    return t === 'okay' || t === 'start' || t.includes('next') || t.includes('continue') || t.includes('play') || t.includes('start module') || t.includes('resume module');
                                });
                                if(btns.length > 0) {
                                    // Check visibility via getBoundingClientRect
                                    const rect = btns[0].getBoundingClientRect();
                                    if(rect.top >= 0 && rect.left >= 0 && rect.width > 0 && rect.height > 0) {
                                        btns[0].click();
                                        return btns[0].innerText;
                                    }
                                }
                                return null;
                            });
                            if (didClick) {
                                console.log(`[Loop] Clicked: "${didClick.trim()}"`);
                            }
                        } catch (err) { }
                    }
                } catch(err) { }
            }
            await delay(3000); 
        }
        console.log("Automation loop finished.");
        await browser.disconnect();
    } catch (e) {
        console.error("Error connecting to Edge:", e.message);
    }
})();
