var os = require('os');
if (os.type().includes('Windows')){
    module.exports=require("../../puppeteer-windows/puppeteer");
}else {
    module.exports=require("../../puppeteer-linux/puppeteer");
}