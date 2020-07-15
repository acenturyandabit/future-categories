let puppeteer = require("./puppeteer.js");
let fs = require("fs");
const cheerio = require('cheerio');
const axios = require('axios');
(async () => {

    let allEntries = [];

    //get all links
    let response = await axios.get(`https://www.futuretimeline.net/21stcentury/21stcentury.htm`);
    let $ = cheerio.load(response.data);
    let allLinks = $("div[id*=decade-box] a.white-small").map((ii, i) => $(i).attr("href").split("#")[0]).get();
    allLinks = Object.keys(allLinks.reduce((p, i) => { p[i] = true; return p }, {})); // dedup
    for (let i of allLinks) {
        //take out all the articles
        let newEntries = [];
        response = await axios.get(i);
        $ = cheerio.load(response.data);
        let e = $(".huge").first();
        let yBracket = e.text();
        let prev = {};
        while (e.next().get(0).tagName == "p") {
            e = e.next();
            if (e.hasClass("huge")) {
                yBracket = e.text();
            } else if (e.hasClass("large")) {
                prev = {};
                newEntries.push(prev);
                prev.title = e.text();
                prev.year = yBracket;
                prev.text = "";
            } else {
                prev.text += e.text();
            }
        }
        allEntries.push.apply(allEntries, newEntries);
        console.log(`retrieved ${newEntries.length} from ${i}`);
    }
    fs.writeFileSync("scraped-axios.json", JSON.stringify(allEntries));
})();