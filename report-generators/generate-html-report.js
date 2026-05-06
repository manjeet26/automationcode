const fs = require('fs');
const path = require('path');

// Read the test results JSON
const testResults = JSON.parse(fs.readFileSync('test-results/test-results.json', 'utf8'));

// Calculate statistics
const totalTests = testResults.tests.length;
const passedTests = testResults.tests.filter(t => t.status === 'PASSED').length;
const failedTests = testResults.tests.filter(t => t.status === 'FAILED').length;
const passRate = ((passedTests / totalTests) * 100).toFixed(1);
const totalDuration = testResults.tests.reduce((sum, t) => sum + t.duration, 0);

// Generate HTML
const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel Test Results</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
            color: #fff;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header .subtitle {
            color: #aaa;
            font-size: 1.1rem;
        }
        
        .header .execution-date {
            margin-top: 15px;
            padding: 10px 20px;
            background: rgba(0, 212, 255, 0.1);
            border-radius: 20px;
            display: inline-block;
            font-size: 0.9rem;
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .stat-card .value {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-card .label {
            color: #aaa;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card.total .value { color: #00d4ff; }
        .stat-card.passed .value { color: #00ff88; }
        .stat-card.failed .value { color: #ff4757; }
        .stat-card.rate .value { color: #ffd700; }
        .stat-card.duration .value { color: #a855f7; font-size: 2rem; }
        
        /* Progress Bar */
        .progress-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .progress-section h3 {
            margin-bottom: 15px;
            color: #00d4ff;
        }
        
        .progress-bar {
            height: 30px;
            background: rgba(255, 71, 87, 0.3);
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00d4ff);
            border-radius: 15px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #1a1a2e;
        }
        
        /* Test Results Table */
        .results-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .results-section h2 {
            margin-bottom: 20px;
            color: #00d4ff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .results-table th {
            background: rgba(0, 212, 255, 0.2);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }
        
        .results-table td {
            padding: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .results-table tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        
        .status-badge.passed {
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            border: 1px solid #00ff88;
        }
        
        .status-badge.failed {
            background: rgba(255, 71, 87, 0.2);
            color: #ff4757;
            border: 1px solid #ff4757;
        }
        
        .duration-badge {
            background: rgba(168, 85, 247, 0.2);
            color: #a855f7;
            padding: 5px 12px;
            border-radius: 10px;
            font-size: 0.85rem;
        }
        
        /* Test Details Cards */
        .test-details {
            margin-top: 30px;
        }
        
        .test-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin-bottom: 20px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .test-card-header {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .test-card-header:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .test-card-header h3 {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .test-number {
            background: linear-gradient(135deg, #00d4ff, #7b2cbf);
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1rem;
        }
        
        .test-card-body {
            padding: 0 20px 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .steps-list {
            list-style: none;
            margin-top: 15px;
        }
        
        .steps-list li {
            padding: 12px 15px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }
        
        .steps-list li.success {
            border-left: 3px solid #00ff88;
        }
        
        .steps-list li.info {
            border-left: 3px solid #00d4ff;
        }
        
        .step-icon {
            font-size: 1.2rem;
        }
        
        /* Screenshot Section */
        .screenshot-section {
            margin-top: 20px;
        }
        
        .screenshot-section h4 {
            color: #aaa;
            margin-bottom: 10px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .screenshot-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: rgba(0, 212, 255, 0.2);
            color: #00d4ff;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .screenshot-link:hover {
            background: rgba(0, 212, 255, 0.3);
            transform: translateX(5px);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-card, .test-card, .results-section {
            animation: fadeIn 0.5s ease forwards;
        }
        
        .stat-card:nth-child(1) { animation-delay: 0.1s; }
        .stat-card:nth-child(2) { animation-delay: 0.2s; }
        .stat-card:nth-child(3) { animation-delay: 0.3s; }
        .stat-card:nth-child(4) { animation-delay: 0.4s; }
        .stat-card:nth-child(5) { animation-delay: 0.5s; }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header h1 { font-size: 1.8rem; }
            .stat-card .value { font-size: 2rem; }
            .results-table { font-size: 0.85rem; }
            .test-card-header { flex-direction: column; gap: 15px; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🧪 Admin Panel Test Results</h1>
            <p class="subtitle">${testResults.testSuite}</p>
            <div class="execution-date">
                📅 Executed on: ${new Date(testResults.executionDate).toLocaleString()}
            </div>
        </div>
        
        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card total">
                <div class="value">${totalTests}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="stat-card passed">
                <div class="value">${passedTests}</div>
                <div class="label">Passed</div>
            </div>
            <div class="stat-card failed">
                <div class="value">${failedTests}</div>
                <div class="label">Failed</div>
            </div>
            <div class="stat-card rate">
                <div class="value">${passRate}%</div>
                <div class="label">Pass Rate</div>
            </div>
            <div class="stat-card duration">
                <div class="value">${(totalDuration / 1000).toFixed(2)}s</div>
                <div class="label">Total Duration</div>
            </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-section">
            <h3>📊 Test Execution Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${passRate}%">
                    ${passRate}% Passed
                </div>
            </div>
        </div>
        
        <!-- Results Summary Table -->
        <div class="results-section">
            <h2>📋 Test Results Summary</h2>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Test Scenario</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Screenshot</th>
                    </tr>
                </thead>
                <tbody>
                    ${testResults.tests.map((test, index) => `
                    <tr>
                        <td><strong>${index + 1}</strong></td>
                        <td>${test.name}</td>
                        <td><span class="status-badge ${test.status.toLowerCase()}">${test.status === 'PASSED' ? '✓ ' : '✗ '}${test.status}</span></td>
                        <td><span class="duration-badge">${test.duration}ms</span></td>
                        <td><a href="${test.screenshot}" class="screenshot-link" target="_blank">📸 View</a></td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        
        <!-- Detailed Test Cards -->
        <div class="results-section test-details">
            <h2>📝 Detailed Test Execution</h2>
            
            ${testResults.tests.map((test, index) => `
            <div class="test-card">
                <div class="test-card-header">
                    <h3>
                        <span class="test-number">${index + 1}</span>
                        ${test.name}
                    </h3>
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <span class="duration-badge">⏱️ ${test.duration}ms</span>
                        <span class="status-badge ${test.status.toLowerCase()}">${test.status === 'PASSED' ? '✓ ' : '✗ '}${test.status}</span>
                    </div>
                </div>
                <div class="test-card-body">
                    <h4 style="color: #aaa; margin-bottom: 10px; font-size: 0.9rem;">EXECUTION STEPS:</h4>
                    <ul class="steps-list">
                        ${test.steps.map(step => `
                        <li class="${step.includes('✓') ? 'success' : 'info'}">
                            <span class="step-icon">${step.includes('✓') ? '✅' : step.includes('✗') ? '❌' : '▶️'}</span>
                            <span>${step}</span>
                        </li>
                        `).join('')}
                    </ul>
                    ${test.error ? `
                    <div style="margin-top: 15px; padding: 15px; background: rgba(255, 71, 87, 0.1); border-radius: 8px; border-left: 3px solid #ff4757;">
                        <strong style="color: #ff4757;">❌ Error:</strong>
                        <p style="margin-top: 8px; color: #ff8a8a;">${test.error}</p>
                    </div>
                    ` : ''}
                    <div class="screenshot-section">
                        <h4>📸 Screenshot Evidence:</h4>
                        <a href="${test.screenshot}" class="screenshot-link" target="_blank">
                            🖼️ ${test.screenshot}
                        </a>
                    </div>
                </div>
            </div>
            `).join('')}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated by Playwright Test Automation | ${new Date().toLocaleString()}</p>
        </div>
    </div>
    
    <script>
        // Add click to expand/collapse functionality
        document.querySelectorAll('.test-card-header').forEach(header => {
            header.addEventListener('click', () => {
                const body = header.nextElementSibling;
                body.style.display = body.style.display === 'none' ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>`;

// Write HTML file
const outputPath = 'test-results/Admin_Panel_Test_Report.html';
fs.writeFileSync(outputPath, html);

console.log(`✅ HTML report generated successfully: ${outputPath}`);
console.log('\nReport Features:');
console.log('  • Modern dark theme with gradient design');
console.log('  • Interactive stats cards with animations');
console.log('  • Visual progress bar showing pass rate');
console.log('  • Summary table with status badges');
console.log('  • Expandable detailed test cards');
console.log('  • Direct links to screenshots');
console.log('  • Fully responsive design');
