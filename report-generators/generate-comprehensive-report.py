#!/usr/bin/env python3
"""
Comprehensive Test Report Generator
Generates detailed HTML reports with logs, metadata, and results
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re


def read_log_file(log_file):
    """Read and parse log file"""
    try:
        with open(log_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Log file not found"


def get_test_logs(log_dir="test-results/logs"):
    """Collect all test logs"""
    logs = {}
    log_path = Path(log_dir)
    
    if log_path.exists():
        for log_file in sorted(log_path.glob("test_*.log")):
            test_name = log_file.stem
            logs[test_name] = read_log_file(str(log_file))
    
    return logs


def parse_pytest_log(log_file="test-results/logs/pytest.log"):
    """Parse pytest log file"""
    try:
        with open(log_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Pytest log file not found"


def get_test_results_summary(log_dir="test-results/logs"):
    """Extract test results summary from logs"""
    pytest_log = parse_pytest_log()
    
    # Extract summary line
    summary_match = re.search(r'(\d+) passed|(\d+) failed|(\d+) error', pytest_log)
    
    summary = {
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'skipped': 0
    }
    
    if 'passed' in pytest_log:
        passed_match = re.search(r'(\d+) passed', pytest_log)
        if passed_match:
            summary['passed'] = int(passed_match.group(1))
    
    if 'failed' in pytest_log:
        failed_match = re.search(r'(\d+) failed', pytest_log)
        if failed_match:
            summary['failed'] = int(failed_match.group(1))
    
    if 'error' in pytest_log:
        error_match = re.search(r'(\d+) error', pytest_log)
        if error_match:
            summary['errors'] = int(error_match.group(1))
    
    return summary


def generate_html_report():
    """Generate comprehensive HTML report"""
    test_logs = get_test_logs()
    pytest_log = parse_pytest_log()
    summary = get_test_results_summary()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Panel Test Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 40px;
                background: #f8f9fa;
            }}
            
            .summary-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            }}
            
            .summary-card.passed {{
                border-left-color: #28a745;
            }}
            
            .summary-card.failed {{
                border-left-color: #dc3545;
            }}
            
            .summary-card.errors {{
                border-left-color: #fd7e14;
            }}
            
            .summary-card.skipped {{
                border-left-color: #ffc107;
            }}
            
            .summary-card .value {{
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
                color: #667eea;
            }}
            
            .summary-card.passed .value {{
                color: #28a745;
            }}
            
            .summary-card.failed .value {{
                color: #dc3545;
            }}
            
            .summary-card.errors .value {{
                color: #fd7e14;
            }}
            
            .summary-card.skipped .value {{
                color: #ffc107;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .section {{
                margin-bottom: 40px;
            }}
            
            .section-title {{
                font-size: 1.8em;
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }}
            
            .logs-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .log-panel {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                overflow: hidden;
            }}
            
            .log-title {{
                background: #667eea;
                color: white;
                padding: 15px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .log-title:hover {{
                background: #764ba2;
            }}
            
            .log-content {{
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 0.85em;
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                display: none;
            }}
            
            .log-content.show {{
                display: block;
            }}
            
            .expand-icon {{
                transition: transform 0.3s ease;
            }}
            
            .expand-icon.open {{
                transform: rotate(180deg);
            }}
            
            .pytest-log {{
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                max-height: 600px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                border-top: 1px solid #dee2e6;
            }}
            
            .metadata {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }}
            
            .metadata-item {{
                padding: 10px;
                background: white;
                border-radius: 4px;
                border-left: 3px solid #667eea;
            }}
            
            .metadata-item label {{
                font-weight: bold;
                color: #667eea;
                display: block;
                margin-bottom: 5px;
            }}
            
            .metadata-item value {{
                color: #333;
            }}
            
            .toggle-btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 20px;
                font-size: 1em;
            }}
            
            .toggle-btn:hover {{
                background: #764ba2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Admin Panel Test Report</h1>
                <p>Comprehensive Test Results & Logs</p>
            </div>
            
            <div class="summary">
                <div class="summary-card passed">
                    <div class="label">✅ Passed</div>
                    <div class="value">{summary['passed']}</div>
                </div>
                <div class="summary-card failed">
                    <div class="label">❌ Failed</div>
                    <div class="value">{summary['failed']}</div>
                </div>
                <div class="summary-card errors">
                    <div class="label">⚠️ Errors</div>
                    <div class="value">{summary['errors']}</div>
                </div>
                <div class="summary-card skipped">
                    <div class="label">⏭️ Skipped</div>
                    <div class="value">{summary['skipped']}</div>
                </div>
            </div>
            
            <div class="content">
                <div class="metadata">
                    <div class="metadata-item">
                        <label>Report Generated</label>
                        <span>{timestamp}</span>
                    </div>
                    <div class="metadata-item">
                        <label>Total Tests</label>
                        <span>{summary['passed'] + summary['failed'] + summary['errors']}</span>
                    </div>
                    <div class="metadata-item">
                        <label>Success Rate</label>
                        <span>{calculate_success_rate(summary)}%</span>
                    </div>
                    <div class="metadata-item">
                        <label>Environment</label>
                        <span>Chromium Browser</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">📋 Test Logs</h2>
                    <button class="toggle-btn" onclick="toggleAllLogs()">Expand All Logs</button>
                    <div class="logs-container">
    """
    
    # Add individual test logs
    for test_name, log_content in sorted(test_logs.items()):
        clean_name = test_name.replace('_', ' ').title()
        html_content += f"""
                        <div class="log-panel">
                            <div class="log-title" onclick="toggleLog(this)">
                                <span>{clean_name}</span>
                                <span class="expand-icon">▼</span>
                            </div>
                            <div class="log-content">
{escape_html(log_content)}
                            </div>
                        </div>
        """
    
    html_content += f"""
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">🔍 Pytest Output</h2>
                    <button class="toggle-btn" onclick="togglePytestLog()">Toggle Pytest Log</button>
                    <div id="pytest-log" class="pytest-log" style="display: none;">
{escape_html(pytest_log)}
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Admin Panel Web Automation Test Suite</p>
                <p>Generated on {timestamp}</p>
            </div>
        </div>
        
        <script>
            function toggleLog(element) {{
                const logContent = element.nextElementSibling;
                const icon = element.querySelector('.expand-icon');
                logContent.classList.toggle('show');
                icon.classList.toggle('open');
            }}
            
            function toggleAllLogs() {{
                const logs = document.querySelectorAll('.log-content');
                const icons = document.querySelectorAll('.expand-icon');
                const allShown = Array.from(logs).every(log => log.classList.contains('show'));
                
                logs.forEach(log => {{
                    if (allShown) {{
                        log.classList.remove('show');
                    }} else {{
                        log.classList.add('show');
                    }}
                }});
                
                icons.forEach(icon => {{
                    if (allShown) {{
                        icon.classList.remove('open');
                    }} else {{
                        icon.classList.add('open');
                    }}
                }});
            }}
            
            function togglePytestLog() {{
                const log = document.getElementById('pytest-log');
                log.style.display = log.style.display === 'none' ? 'block' : 'none';
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def calculate_success_rate(summary):
    """Calculate test success rate"""
    total = sum(summary.values())
    if total == 0:
        return 0
    success_rate = (summary['passed'] / total) * 100
    return round(success_rate, 2)


def main():
    """Generate and save report"""
    print("🔨 Generating comprehensive test report...")
    
    # Ensure output directory exists
    Path("test-results").mkdir(exist_ok=True)
    
    # Generate HTML report
    html_content = generate_html_report()
    
    # Save report
    report_path = "test-results/comprehensive-test-report.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report generated successfully: {report_path}")
    print(f"📊 Open the report in your browser to view detailed test results and logs")


if __name__ == "__main__":
    main()
