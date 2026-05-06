const { chromium } = require('playwright');
const fs = require('fs');

async function testLogoutPopup() {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Login first
  await page.goto('https://adminauctionqa.gaadi.com', { waitUntil: 'networkidle', timeout: 30000 });
  await page.fill('input[name="username"].sign-txtbox', 'administrator');
  await page.fill('input[name="password"].sign-txtbox', 'testing');
  await page.click('button:has-text("SIGN IN")');
  await page.waitForURL('**/auction/manageAuction**', { timeout: 15000 });
  
  console.log('Logged in. Opening dropdown...');
  
  // Open dropdown via JS
  await page.evaluate(() => {
    const dropdown = document.querySelector('.login-btn-mob');
    if (dropdown) {
      dropdown.classList.add('open');
      const menu = dropdown.querySelector('.dropdown-menu');
      if (menu) menu.style.display = 'block';
    }
  });
  await page.waitForTimeout(500);
  
  // Click logout
  console.log('Clicking logout...');
  await page.click('.login-btn-mob .confirm_logout', { force: true });
  
  // Wait for popup
  await page.waitForTimeout(2000);
  
  // Take screenshot of popup
  await page.screenshot({ path: 'screenshots/logout-popup.png', fullPage: true });
  console.log('Screenshot saved: screenshots/logout-popup.png');
  
  // Get all visible buttons/elements
  const buttons = await page.$$eval('button, .btn, [role="button"]', elements => 
    elements.filter(el => el.offsetParent !== null).map(el => ({
      tag: el.tagName,
      text: el.textContent?.trim(),
      className: el.className,
      id: el.id
    }))
  );
  
  console.log('\n=== VISIBLE BUTTONS ===');
  console.log(JSON.stringify(buttons, null, 2));
  
  // Check for modal/popup
  const modals = await page.$$eval('.modal, .popup, .dialog, [role="dialog"], .bootbox, .swal2-container, .sweet-alert', elements => 
    elements.map(el => ({
      tag: el.tagName,
      className: el.className,
      visible: el.offsetParent !== null,
      innerHTML: el.innerHTML.substring(0, 500)
    }))
  );
  
  console.log('\n=== MODALS/POPUPS ===');
  console.log(JSON.stringify(modals, null, 2));
  
  await browser.close();
}

testLogoutPopup().catch(console.error);
