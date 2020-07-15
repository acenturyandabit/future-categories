let puppeteer = require("./puppeteer.js");
let fs = require("fs");
(async () => {
    let browser = await puppeteer.launch({ headless: false });
    let p = await browser.newPage();
    let startYear = 0;
    let allEntries = [];
    while (startYear < 100) {
        await p.goto(`https://www.futuretimeline.net/${21 + Math.floor(startYear / 100)}stcentury/${2000 + startYear}-${2009 + startYear}.htm`, { waitUntil: "load" });
        let entries = await p.$$eval("a.white", (els) => {
            return els.map(i => {
                let u = i;
                while (u.tagName != "P") u = u.parentElement;
                return {
                    name: i.innerText,
                    year: u.previousElementSibling.innerText
                }
            })
        })
        allEntries.push.apply(allEntries, entries);
        startYear += 10;
    }
    fs.writeFileSync("scraped.json", JSON.stringify(allEntries));
})();