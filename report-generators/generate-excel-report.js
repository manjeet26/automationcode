const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

// Read the test results JSON
const testResults = JSON.parse(fs.readFileSync('test-results/test-results.json', 'utf8'));

// Create workbook
const workbook = XLSX.utils.book_new();

// ============================================
// Sheet 1: Summary
// ============================================
const summaryData = [
  ['Admin Panel Test Results - Summary Report'],
  [],
  ['Test Suite:', testResults.testSuite],
  ['Execution Date:', new Date(testResults.executionDate).toLocaleString()],
  ['Total Tests:', testResults.tests.length],
  ['Passed:', testResults.tests.filter(t => t.status === 'PASSED').length],
  ['Failed:', testResults.tests.filter(t => t.status === 'FAILED').length],
  ['Pass Rate:', `${((testResults.tests.filter(t => t.status === 'PASSED').length / testResults.tests.length) * 100).toFixed(1)}%`],
  [],
  ['#', 'Test Scenario', 'Status', 'Duration (ms)', 'Screenshot']
];

testResults.tests.forEach((test, index) => {
  summaryData.push([
    index + 1,
    test.name,
    test.status,
    test.duration,
    test.screenshot
  ]);
});

const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);

// Set column widths for summary sheet
summarySheet['!cols'] = [
  { wch: 5 },   // #
  { wch: 60 },  // Test Scenario
  { wch: 10 },  // Status
  { wch: 15 }, // Duration
  { wch: 40 }   // Screenshot
];

XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary');

// ============================================
// Sheet 2: Detailed Results
// ============================================
const detailedData = [
  ['Admin Panel Test Results - Detailed Report'],
  [],
  ['Scenario #', 'Scenario Name', 'Status', 'Duration (ms)', 'Step #', 'Step Description', 'Error']
];

testResults.tests.forEach((test, testIndex) => {
  test.steps.forEach((step, stepIndex) => {
    detailedData.push([
      stepIndex === 0 ? testIndex + 1 : '',
      stepIndex === 0 ? test.name : '',
      stepIndex === 0 ? test.status : '',
      stepIndex === 0 ? test.duration : '',
      stepIndex + 1,
      step,
      stepIndex === 0 && test.error ? test.error : ''
    ]);
  });
  // Add empty row between scenarios
  detailedData.push([]);
});

const detailedSheet = XLSX.utils.aoa_to_sheet(detailedData);

// Set column widths for detailed sheet
detailedSheet['!cols'] = [
  { wch: 12 },  // Scenario #
  { wch: 55 },  // Scenario Name
  { wch: 10 },  // Status
  { wch: 15 },  // Duration
  { wch: 8 },   // Step #
  { wch: 80 },  // Step Description
  { wch: 50 }   // Error
];

XLSX.utils.book_append_sheet(workbook, detailedSheet, 'Detailed Results');

// ============================================
// Sheet 3: Test Cases
// ============================================
const testCasesData = [
  ['Test Case ID', 'Test Case Name', 'Preconditions', 'Test Steps', 'Expected Result', 'Actual Result', 'Status', 'Screenshot'],
  [
    'TC_001',
    'Verify admin Panel login functionality with valid credentials',
    'Admin Panel URL is accessible',
    '1. Navigate to Admin Panel: https://adminauctionqa.gaadi.com\n2. Enter Username: administrator\n3. Enter Password: testing\n4. Click Login button',
    'User should be logged in and redirected to Auctions page (https://adminauctionqa.gaadi.com/auction/manageAuction)',
    testResults.tests[0].steps.filter(s => s.includes('✓')).join('\n'),
    testResults.tests[0].status,
    testResults.tests[0].screenshot
  ],
  [
    'TC_002',
    'Verify admin Panel login functionality with invalid credentials',
    'Admin Panel URL is accessible',
    '1. Navigate to Admin Panel: https://adminauctionqa.gaadi.com\n2. Enter Username: administrator\n3. Enter Password: testing@123 (invalid)\n4. Click Login button',
    'User should NOT be logged in and validation error message should appear',
    testResults.tests[1].steps.filter(s => s.includes('✓')).join('\n'),
    testResults.tests[1].status,
    testResults.tests[1].screenshot
  ],
  [
    'TC_003',
    'Verify admin Panel logout functionality',
    'User is logged into Admin Panel',
    '1. Navigate to Admin Panel: https://adminauctionqa.gaadi.com\n2. Login with valid credentials (administrator/testing)\n3. Click on user dropdown in top-right corner\n4. Click on Logout option\n5. Accept confirmation popup',
    'User should be logged out and redirected to login page (https://adminauctionqa.gaadi.com/)',
    testResults.tests[2].steps.filter(s => s.includes('✓')).join('\n'),
    testResults.tests[2].status,
    testResults.tests[2].screenshot
  ]
];

const testCasesSheet = XLSX.utils.aoa_to_sheet(testCasesData);

// Set column widths for test cases sheet
testCasesSheet['!cols'] = [
  { wch: 12 },  // Test Case ID
  { wch: 55 },  // Test Case Name
  { wch: 30 },  // Preconditions
  { wch: 60 },  // Test Steps
  { wch: 50 },  // Expected Result
  { wch: 50 },  // Actual Result
  { wch: 10 },  // Status
  { wch: 40 }   // Screenshot
];

XLSX.utils.book_append_sheet(workbook, testCasesSheet, 'Test Cases');

// ============================================
// Write the Excel file
// ============================================
const outputPath = 'test-results/Admin_Panel_Test_Results.xlsx';
XLSX.writeFile(workbook, outputPath);

console.log(`✅ Excel report generated successfully: ${outputPath}`);
console.log('\nSheets created:');
console.log('  1. Summary - Overview of test execution');
console.log('  2. Detailed Results - Step-by-step execution details');
console.log('  3. Test Cases - Formal test case documentation');
