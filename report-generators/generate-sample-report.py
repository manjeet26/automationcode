#!/usr/bin/env python3
"""
Generate HTML report from pytest JSON results
"""

import json
import os
from datetime import datetime
from pathlib import Path


TEST_DESCRIPTIONS = {
    "test_login_page_loads": "Verify login page loads with all required elements visible",
    "test_invalid_login": "Verify login is blocked with invalid credentials on practice site",
    "test_logout_functionality": "Verify admin user can successfully logout from the admin panel",
    "test_smoke_admin_login_page_loads": "Verify admin login page loads with all required elements visible",
    "test_smoke_admin_login_with_valid_credentials": "Verify successful login with valid admin credentials and redirect to auction management page",
    "test_smoke_admin_login_with_invalid_credentials_is_blocked": "Verify login is blocked when invalid credentials are provided",
    "test_smoke_admin_logout": "Verify admin user logout functionality and redirect back to login page",
}


def get_test_name(nodeid):
    return nodeid.split("::")[-1].replace("[chromium]", "")


def load_test_results(json_path="test-results/test-results.json"):
    with open(json_path) as f:
        return json.load(f)


def escape_html(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def load_test_logs(log_dir="test-results/logs"):
    logs = {}
    log_path = Path(log_dir)
    if log_path.exists():
        for log_file in sorted(log_path.glob("test_*.log")):
            test_name = log_file.stem.replace("[chromium]", "")
            try:
                with open(log_file, 'r') as f:
                    logs[test_name] = f.read()
            except FileNotFoundError:
                pass
    return logs


def generate_report():
    results = load_test_results()
    test_logs = load_test_logs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = results.get("summary", {})
    total_passed = summary.get("passed", 0)
    total_failed = summary.get("failed", 0)
    total_errors = summary.get("error", 0)
    total_tests = summary.get("total", 0)
    total_duration = results.get("duration", 0)

    if total_tests > 0:
        success_rate = round((total_passed / total_tests) * 100, 1)
    else:
        success_rate = 0

    test_results_html = ""
    summary_rows = ""
    logs_html = ""

    for test in results.get("tests", []):
        nodeid = test["nodeid"]
        outcome = test["outcome"]
        call_duration = test.get("call", {}).get("duration", 0) or 0
        test_name = get_test_name(nodeid)
        status_class = "passed" if outcome == "passed" else "failed"
        status_text = "PASSED" if outcome == "passed" else "FAILED"
        icon = "✅" if outcome == "passed" else "❌"
        description = TEST_DESCRIPTIONS.get(test_name, "No description available")

        test_results_html += f"""
                    <div class="test-result {status_class}">
                        <div class="test-name">
                            <span class="icon">{icon}</span>
                            {test_name}
                        </div>
                        <div class="test-details">
                            <strong>Status:</strong> <span class="status-{status_class}">{status_text}</span>
                            <strong>Duration:</strong> <span class="duration">{call_duration:.2f}s</span>
                            <strong>Description:</strong> <span>{description}</span>
                        </div>
                    </div>
        """

        ts = datetime.now().strftime("%H:%M:%S")
        summary_rows += f"""
                        <tr>
                            <td>{test_name}</td>
                            <td class="status-{status_class}">{status_text}</td>
                            <td>{call_duration:.2f}s</td>
                            <td>{ts}</td>
                        </tr>
        """

    for test_name, log_content in sorted(test_logs.items()):
        logs_html += f"""
        <div style="margin-bottom: 20px;">
            <strong style="color: #667eea; font-size: 1.1em;">{test_name.replace('_', ' ').title()}</strong>
            <div class="log-content" style="margin-top: 8px;">{escape_html(log_content)}</div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel Test Results Report</title>
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

        .test-results {{
            display: grid;
            gap: 20px;
        }}

        .test-result {{
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            background: #f0f9ff;
        }}

        .test-result.passed {{
            background: #f0fdf4;
            border-left-color: #28a745;
        }}

        .test-result.failed {{
            background: #fef2f2;
            border-left-color: #dc3545;
        }}

        .test-result.error {{
            background: #fff7ed;
            border-left-color: #fd7e14;
        }}

        .test-name {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .test-name .icon {{
            font-size: 1.5em;
        }}

        .test-details {{
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 15px;
            font-size: 0.95em;
            color: #666;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }}

        .test-details strong {{
            color: #333;
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

        .duration {{
            color: #999;
            font-size: 0.9em;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .status-passed {{
            color: #28a745;
            font-weight: bold;
        }}

        .status-failed {{
            color: #dc3545;
            font-weight: bold;
        }}

        .log-content {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Admin Panel Test Results</h1>
            <p>Comprehensive Test Report</p>
        </div>

        <div class="summary">
            <div class="summary-card passed">
                <div class="label">Passed</div>
                <div class="value">{total_passed}</div>
            </div>
            <div class="summary-card failed">
                <div class="label">Failed</div>
                <div class="value">{total_failed}</div>
            </div>
            <div class="summary-card errors">
                <div class="label">Errors</div>
                <div class="value">{total_errors}</div>
            </div>
            <div class="summary-card">
                <div class="label">Success Rate</div>
                <div class="value" style="color: #28a745;">{success_rate}%</div>
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
                    <span>{total_tests}</span>
                </div>
                <div class="metadata-item">
                    <label>Total Duration</label>
                    <span>{total_duration:.2f} seconds</span>
                </div>
                <div class="metadata-item">
                    <label>Environment</label>
                    <span>Chromium Browser</span>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Test Results</h2>
                <div class="test-results">
{test_results_html}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Summary Table</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            <th>Status</th>
                            <th>Duration</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
{summary_rows}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Detailed Logs</h2>
{logs_html}
            </div>
        </div>

        <div class="footer">
            <p>Admin Panel Web Automation Test Suite</p>
            <p>Generated on {timestamp}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <strong>Report Location:</strong> test-results/sample-test-results.html
            </p>
        </div>
    </div>
</body>
</html>"""

    return html_content


def main():
    print("Generating test results HTML report...")

    html_content = generate_report()

    Path("test-results").mkdir(exist_ok=True)
    report_path = "test-results/sample-test-results.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
