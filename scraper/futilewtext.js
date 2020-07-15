let puppeteer = require("./puppeteer.js");
let fs = require("fs");

(async () => {
    let browser = await puppeteer.launch({ headless: false });
    let p = await browser.newPage();

    let allEntries = [];

    //get all links
    await p.goto(`https://www.futuretimeline.net/21stcentury/21stcentury.htm`, { waitUntil: "load" });
    let allLinks = await p.$$eval("div[id*=decade-box] a.white-small", (els) => els.map(i => i.href.split("#")[0]));
    allLinks = Object.keys(allLinks.reduce((p, i) => { p[i] = true; return p }, {})); // dedup
    for (let i of allLinks) {
        await p.goto(i, { waitUntil: "load" });
        //take out all the articles
        let newEntries = await p.$eval(".huge", (e) => {
            let result = [];
            let yBracket = e.innerText;
            let prev = {};
            while (e.nextElementSibling.tagName == "P") {
                e = e.nextElementSibling;
                if (e.classList.contains("huge")) {
                    yBracket = e.innerText;
                } else if (e.classList.contains("large")) {
                    prev = {};
                    result.push(prev);
                    prev.title = e.innerText;
                    prev.year = yBracket;
                    prev.text = "";
                } else {
                    prev.text += e.innerText;
                }
            }
            return result;
        })
        allEntries.push.apply(allEntries, newEntries);
    }
    fs.writeFileSync("scraped-wtext.json", JSON.stringify(allEntries));
})();