const { chromium } = require('playwright');
const fs = require('fs');

// Test Results Storage
const testResults = {
  testSuite: 'Admin Panel Login/Logout Tests',
  executionDate: new Date().toISOString(),
  tests: []
};

// Helper function to save results
function saveResults() {
  fs.writeFileSync('test-results/test-results.json', JSON.stringify(testResults, null, 2));
}

// Helper function to generate markdown report
function generateMarkdownReport() {
  let report = `# Admin Panel Test Results\n\n`;
  report += `**Execution Date:** ${testResults.executionDate}\n\n`;
  report += `| # | Test Scenario | Status | Duration | Screenshot |\n`;
  report += `|---|---------------|--------|----------|------------|\n`;
  
  testResults.tests.forEach((test, index) => {
    const statusEmoji = test.status === 'PASSED' ? '✅' : '❌';
    report += `| ${index + 1} | ${test.name} | ${statusEmoji} ${test.status} | ${test.duration}ms | [View](${test.screenshot}) |\n`;
  });
  
  report += `\n## Detailed Results\n\n`;
  testResults.tests.forEach((test, index) => {
    report += `### Scenario ${index + 1}: ${test.name}\n\n`;
    report += `- **Status:** ${test.status}\n`;
    report += `- **Duration:** ${test.duration}ms\n`;
    report += `- **Screenshot:** ${test.screenshot}\n`;
    if (test.error) {
      report += `- **Error:** ${test.error}\n`;
    }
    report += `- **Steps:**\n`;
    test.steps.forEach(step => {
      report += `  - ${step}\n`;
    });
    report += `\n`;
  });
  
  fs.writeFileSync('test-results/test-report.md', report);
}

async function runTests() {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  // ============================================
  // SCENARIO 1: Valid Login
  // ============================================
  console.log('\n' + '='.repeat(60));
  console.log('SCENARIO 1: Verify admin Panel login with valid credentials');
  console.log('='.repeat(60));
  
  let test1 = {
    name: 'Verify admin Panel login functionality with valid credentials',
    steps: [],
    status: 'PENDING',
    screenshot: '',
    duration: 0,
    error: null
  };
  
  const startTime1 = Date.now();
  const context1 = await browser.newContext();
  const page1 = await context1.newPage();
  
  try {
    // Step 1: Navigate to Admin Panel
    test1.steps.push('Navigate to Admin Panel: https://adminauctionqa.gaadi.com');
    console.log('Step 1: Navigating to Admin Panel...');
    await page1.goto('https://adminauctionqa.gaadi.com', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('  ✓ Navigation successful');
    
    // Step 2: Enter Username
    test1.steps.push('Enter Username: administrator');
    console.log('Step 2: Entering username...');
    await page1.waitForSelector('input[name="username"].sign-txtbox', { timeout: 10000 });
    await page1.fill('input[name="username"].sign-txtbox', 'administrator');
    console.log('  ✓ Username entered');
    
    // Step 3: Enter Password
    test1.steps.push('Enter Password: testing');
    console.log('Step 3: Entering password...');
    await page1.fill('input[name="password"].sign-txtbox', 'testing');
    console.log('  ✓ Password entered');
    
    // Step 4: Click Login Button
    test1.steps.push('Click Login button');
    console.log('Step 4: Clicking login button...');
    await page1.click('button:has-text("SIGN IN")');
    console.log('  ✓ Login button clicked');
    
    // Step 5: Wait for navigation and verify URL
    test1.steps.push('Verify redirect to Auctions page');
    console.log('Step 5: Verifying redirect to Auctions page...');
    await page1.waitForURL('**/auction/manageAuction**', { timeout: 15000 });
    const currentUrl = page1.url();
    
    if (currentUrl.includes('/auction/manageAuction')) {
      test1.steps.push(`✓ Successfully redirected to: ${currentUrl}`);
      console.log(`  ✓ Successfully redirected to: ${currentUrl}`);
      test1.status = 'PASSED';
    } else {
      throw new Error(`Expected URL containing /auction/manageAuction but got: ${currentUrl}`);
    }
    
  } catch (error) {
    test1.status = 'FAILED';
    test1.error = error.message;
    test1.steps.push(`✗ Error: ${error.message}`);
    console.log(`  ✗ Error: ${error.message}`);
  }
  
  // Take screenshot
  test1.screenshot = 'screenshots/scenario1-valid-login.png';
  await page1.screenshot({ path: test1.screenshot, fullPage: true });
  console.log(`Screenshot saved: ${test1.screenshot}`);
  
  test1.duration = Date.now() - startTime1;
  testResults.tests.push(test1);
  saveResults();
  
  console.log(`\nScenario 1 Result: ${test1.status} (${test1.duration}ms)`);
  
  await context1.close();
  
  // ============================================
  // SCENARIO 2: Invalid Login
  // ============================================
  console.log('\n' + '='.repeat(60));
  console.log('SCENARIO 2: Verify admin Panel login with invalid credentials');
  console.log('='.repeat(60));
  
  let test2 = {
    name: 'Verify admin Panel login functionality with invalid credentials',
    steps: [],
    status: 'PENDING',
    screenshot: '',
    duration: 0,
    error: null
  };
  
  const startTime2 = Date.now();
  const context2 = await browser.newContext();
  const page2 = await context2.newPage();
  
  try {
    // Step 1: Navigate to Admin Panel
    test2.steps.push('Navigate to Admin Panel: https://adminauctionqa.gaadi.com');
    console.log('Step 1: Navigating to Admin Panel...');
    await page2.goto('https://adminauctionqa.gaadi.com', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('  ✓ Navigation successful');
    
    // Step 2: Enter Username
    test2.steps.push('Enter Username: administrator');
    console.log('Step 2: Entering username...');
    await page2.waitForSelector('input[name="username"].sign-txtbox', { timeout: 10000 });
    await page2.fill('input[name="username"].sign-txtbox', 'administrator');
    console.log('  ✓ Username entered');
    
    // Step 3: Enter Invalid Password
    test2.steps.push('Enter Invalid Password: testing@123');
    console.log('Step 3: Entering invalid password...');
    await page2.fill('input[name="password"].sign-txtbox', 'testing@123');
    console.log('  ✓ Invalid password entered');
    
    // Step 4: Click Login Button
    test2.steps.push('Click Login button');
    console.log('Step 4: Clicking login button...');
    await page2.click('button:has-text("SIGN IN")');
    console.log('  ✓ Login button clicked');
    
    // Step 5: Verify error message appears
    test2.steps.push('Verify validation error message appears');
    console.log('Step 5: Verifying error message...');
    await page2.waitForTimeout(2000); // Wait for error to appear
    
    // Check for various error message patterns
    const errorSelectors = [
      '.error', '.alert', '.error-message', '.validation-error',
      '[class*="error"]', '[class*="alert"]', '.toast-error',
      'text=Invalid', 'text=incorrect', 'text=wrong', 'text=failed'
    ];
    
    let errorFound = false;
    let errorText = '';
    
    for (const selector of errorSelectors) {
      try {
        const errorElement = await page2.$(selector);
        if (errorElement) {
          errorText = await errorElement.textContent();
          if (errorText && errorText.trim().length > 0) {
            errorFound = true;
            break;
          }
        }
      } catch (e) {
        // Continue checking other selectors
      }
    }
    
    // Also check if we're still on login page (not redirected)
    const currentUrl2 = page2.url();
    const stillOnLoginPage = !currentUrl2.includes('/auction/manageAuction');
    
    if (errorFound || stillOnLoginPage) {
      test2.steps.push(`✓ Login blocked - User remains on login page`);
      if (errorText) {
        test2.steps.push(`✓ Error message displayed: "${errorText.trim()}"`);
      }
      console.log(`  ✓ Login blocked - User remains on login page`);
      if (errorText) {
        console.log(`  ✓ Error message: "${errorText.trim()}"`);
      }
      test2.status = 'PASSED';
    } else {
      throw new Error('Login was not blocked - user may have been redirected');
    }
    
  } catch (error) {
    test2.status = 'FAILED';
    test2.error = error.message;
    test2.steps.push(`✗ Error: ${error.message}`);
    console.log(`  ✗ Error: ${error.message}`);
  }
  
  // Take screenshot
  test2.screenshot = 'screenshots/scenario2-invalid-login.png';
  await page2.screenshot({ path: test2.screenshot, fullPage: true });
  console.log(`Screenshot saved: ${test2.screenshot}`);
  
  test2.duration = Date.now() - startTime2;
  testResults.tests.push(test2);
  saveResults();
  
  console.log(`\nScenario 2 Result: ${test2.status} (${test2.duration}ms)`);
  
  await context2.close();
  
  // ============================================
  // SCENARIO 3: Logout Functionality
  // ============================================
  console.log('\n' + '='.repeat(60));
  console.log('SCENARIO 3: Verify admin Panel logout functionality');
  console.log('='.repeat(60));
  
  let test3 = {
    name: 'Verify admin Panel logout functionality',
    steps: [],
    status: 'PENDING',
    screenshot: '',
    duration: 0,
    error: null
  };
  
  const startTime3 = Date.now();
  const context3 = await browser.newContext();
  const page3 = await context3.newPage();
  
  try {
    // Step 1: Navigate to Admin Panel
    test3.steps.push('Navigate to Admin Panel: https://adminauctionqa.gaadi.com');
    console.log('Step 1: Navigating to Admin Panel...');
    await page3.goto('https://adminauctionqa.gaadi.com', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('  ✓ Navigation successful');
    
    // Step 2: Login with valid credentials
    test3.steps.push('Login with valid credentials (administrator/testing)');
    console.log('Step 2: Logging in with valid credentials...');
    
    await page3.waitForSelector('input[name="username"].sign-txtbox', { timeout: 10000 });
    await page3.fill('input[name="username"].sign-txtbox', 'administrator');
    await page3.fill('input[name="password"].sign-txtbox', 'testing');
    await page3.click('button:has-text("SIGN IN")');
    
    await page3.waitForURL('**/auction/manageAuction**', { timeout: 15000 });
    console.log('  ✓ Login successful');
    
    // Step 3: Click on user dropdown in top-right
    test3.steps.push('Click on user dropdown in top-right corner');
    console.log('Step 3: Clicking on user dropdown...');
    
    // Set up dialog handler BEFORE clicking logout (for native confirm dialog)
    page3.on('dialog', async dialog => {
      console.log(`  Dialog appeared: ${dialog.type()} - "${dialog.message()}"`);
      await dialog.accept();
      console.log('  ✓ Dialog accepted');
    });
    
    // Use JavaScript to show the dropdown menu
    await page3.evaluate(() => {
      const dropdown = document.querySelector('.login-btn-mob');
      if (dropdown) {
        dropdown.classList.add('open');
        const menu = dropdown.querySelector('.dropdown-menu');
        if (menu) menu.style.display = 'block';
      }
    });
    await page3.waitForTimeout(500);
    console.log('  ✓ Dropdown opened');
    
    // Step 4: Click Logout option
    test3.steps.push('Click on Logout option');
    console.log('Step 4: Clicking Logout option...');
    
    // Click the visible logout link
    await page3.click('.login-btn-mob .confirm_logout', { force: true });
    console.log('  ✓ Logout option clicked');
    
    // Step 5: Wait for dialog and redirect
    test3.steps.push('Accept confirmation popup');
    console.log('Step 5: Waiting for confirmation and redirect...');
    
    // Wait for the page to redirect after dialog acceptance
    await page3.waitForTimeout(3000);
    
    // Step 6: Verify redirect to login page
    test3.steps.push('Verify redirect to login page');
    console.log('Step 6: Verifying redirect to login page...');
    
    await page3.waitForTimeout(2000);
    await page3.waitForURL('**/adminauctionqa.gaadi.com/**', { timeout: 15000 });
    
    const finalUrl = page3.url();
    const isOnLoginPage = finalUrl === 'https://adminauctionqa.gaadi.com/' || 
                          finalUrl === 'https://adminauctionqa.gaadi.com' ||
                          !finalUrl.includes('/auction/manageAuction');
    
    if (isOnLoginPage) {
      test3.steps.push(`✓ Successfully logged out and redirected to: ${finalUrl}`);
      console.log(`  ✓ Successfully logged out and redirected to: ${finalUrl}`);
      test3.status = 'PASSED';
    } else {
      throw new Error(`Expected redirect to login page but got: ${finalUrl}`);
    }
    
  } catch (error) {
    test3.status = 'FAILED';
    test3.error = error.message;
    test3.steps.push(`✗ Error: ${error.message}`);
    console.log(`  ✗ Error: ${error.message}`);
  }
  
  // Take screenshot
  test3.screenshot = 'screenshots/scenario3-logout.png';
  await page3.screenshot({ path: test3.screenshot, fullPage: true });
  console.log(`Screenshot saved: ${test3.screenshot}`);
  
  test3.duration = Date.now() - startTime3;
  testResults.tests.push(test3);
  saveResults();
  
  console.log(`\nScenario 3 Result: ${test3.status} (${test3.duration}ms)`);
  
  await context3.close();
  await browser.close();
  
  // Generate final report
  generateMarkdownReport();
  
  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('TEST EXECUTION SUMMARY');
  console.log('='.repeat(60));
  
  const passed = testResults.tests.filter(t => t.status === 'PASSED').length;
  const failed = testResults.tests.filter(t => t.status === 'FAILED').length;
  
  testResults.tests.forEach((test, index) => {
    const icon = test.status === 'PASSED' ? '✅' : '❌';
    console.log(`${icon} Scenario ${index + 1}: ${test.name} - ${test.status}`);
  });
  
  console.log('\n' + '-'.repeat(60));
  console.log(`Total: ${testResults.tests.length} | Passed: ${passed} | Failed: ${failed}`);
  console.log('='.repeat(60));
  console.log('\nTest results saved to: test-results/test-results.json');
  console.log('Test report saved to: test-results/test-report.md');
  console.log('Screenshots saved to: screenshots/');
}

runTests().catch(console.error);
