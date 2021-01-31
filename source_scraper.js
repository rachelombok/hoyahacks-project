//Selenium Web Driver scraping tool
const {Builder, By} = require('selenium-webdriver');
const webdriver = require('selenium-webdriver');
const safari = require('selenium-webdriver/safari');
async function main(){
    //builds driver and sends to website.
    let driver  =  new Builder().forBrowser('safari').build();
    driver.manage().setTimeouts({implicit: 10000});
    await driver.get("https://www.adfontesmedia.com/rankings-by-individual-news-source/");
    let source_names = await driver.findElements(By.className("blog-shortcode-post-title entry-title fusion-responsive-typography-calculated"));
    let i = await 0;
    let total = await source_names.length;
    for (i = 0; i < total; i++) {
	//finds all the source names... Really slow because selenium won't let me save the data when I switch pages
	let source_names = await driver.findElements(By.className("blog-shortcode-post-title entry-title fusion-responsive-typography-calculated"));
	//then go to each sources link on the website
        let name = await source_names[i].getText();
	let source_link = await driver.findElement(By.linkText(name));
	let link = await source_link.getAttribute("href");
	await driver.get(link);
	//get the body of the text that contains the important info
	let page = await driver.findElement(By.className("fusion-text fusion-text-1"));
	let attributes = await page.getText();
	attributes = await attributes.split(" ");
	await attributes.splice(0,100);
	//find reliability and bias from the text
	let reliability = "", bias = "";
	for (k = 0; k < attributes.length; k++) {
	    if (attributes[k] == "methodology.Reliability:") {
		reliability = await attributes[k+1];
		bias = await attributes[k+2];
		k = await attributes.length + 1;
	    }
	}
	reliability = await reliability.replace("Bias:", "");
	bias = await bias.replace("Reliability", "");
	name = await name.replace(" Bias and Reliability", "");
	await console.log('"' + name + '"'  + ", " + reliability + ", " + bias);
	await driver.get("https://www.adfontesmedia.com/rankings-by-individual-news-source/");
    }
}

main();
