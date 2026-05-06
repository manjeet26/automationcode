const { chromium } = require('playwright');
const fs = require('fs');

async function inspectPage() {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://adminauctionqa.gaadi.com', { waitUntil: 'networkidle', timeout: 30000 });
  
  // Get all input elements
  const inputs = await page.$$eval('input', elements => 
    elements.map(el => ({
      type: el.type,
      name: el.name,
      id: el.id,
      placeholder: el.placeholder,
      className: el.className,
      visible: el.offsetParent !== null
    }))
  );
  
  console.log('=== INPUT ELEMENTS ===');
  console.log(JSON.stringify(inputs, null, 2));
  
  // Get all buttons
  const buttons = await page.$$eval('button, input[type="submit"]', elements => 
    elements.map(el => ({
      type: el.type,
      text: el.textContent?.trim(),
      className: el.className,
      id: el.id
    }))
  );
  
  console.log('\n=== BUTTONS ===');
  console.log(JSON.stringify(buttons, null, 2));
  
  // Get page HTML structure
  const html = await page.content();
  fs.writeFileSync('page-structure.html', html);
  console.log('\nPage HTML saved to page-structure.html');
  
  await browser.close();
}

inspectPage().catch(console.error);
