const { chromium } = require('playwright');
const fs = require('fs');

async function inspectLoggedInPage() {
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
  
  console.log('Logged in successfully. Inspecting page...\n');
  
  // Get all dropdown elements
  const dropdowns = await page.$$eval('[class*="dropdown"], .nav-item, .navbar-nav > li', elements => 
    elements.map(el => ({
      tag: el.tagName,
      className: el.className,
      id: el.id,
      text: el.textContent?.trim().substring(0, 100)
    }))
  );
  
  console.log('=== DROPDOWN ELEMENTS ===');
  console.log(JSON.stringify(dropdowns, null, 2));
  
  // Get all links with logout
  const logoutLinks = await page.$$eval('a, button', elements => 
    elements.filter(el => 
      el.textContent?.toLowerCase().includes('logout') || 
      el.textContent?.toLowerCase().includes('log out') ||
      el.textContent?.toLowerCase().includes('sign out') ||
      el.href?.toLowerCase().includes('logout')
    ).map(el => ({
      tag: el.tagName,
      text: el.textContent?.trim(),
      href: el.href,
      className: el.className,
      id: el.id
    }))
  );
  
  console.log('\n=== LOGOUT LINKS ===');
  console.log(JSON.stringify(logoutLinks, null, 2));
  
  // Get navbar structure
  const navbar = await page.$$eval('.navbar, nav, header', elements => 
    elements.map(el => ({
      tag: el.tagName,
      className: el.className,
      innerHTML: el.innerHTML.substring(0, 2000)
    }))
  );
  
  console.log('\n=== NAVBAR STRUCTURE ===');
  navbar.forEach((n, i) => {
    console.log(`\n--- Element ${i + 1} (${n.tag}.${n.className}) ---`);
    console.log(n.innerHTML);
  });
  
  // Save full HTML
  const html = await page.content();
  fs.writeFileSync('logged-in-page.html', html);
  console.log('\n\nFull HTML saved to logged-in-page.html');
  
  // Take screenshot
  await page.screenshot({ path: 'screenshots/logged-in-inspect.png', fullPage: true });
  console.log('Screenshot saved to screenshots/logged-in-inspect.png');
  
  await browser.close();
}

inspectLoggedInPage().catch(console.error);
