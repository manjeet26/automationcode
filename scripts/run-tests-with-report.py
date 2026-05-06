#!/usr/bin/env python3
"""
Test Runner with Comprehensive Logging and Report Generation
Runs tests with detailed logging and generates comprehensive reports
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

SEPARATOR = "=" * 80
REPORT_DIR = "test-results"
LOG_DIR = f"{REPORT_DIR}/logs"


def run_tests() -> int:
    """Run pytest with detailed logging"""
    print(SEPARATOR)
    print("🚀 Starting Admin Panel Test Suite")
    print(SEPARATOR)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Ensure log directory exists
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    
    # Run pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--log-cli=true",
        "--log-cli-level=INFO",
        f"--log-file={LOG_DIR}/pytest.log",
        "--log-file-level=DEBUG",
    ]
    
    print(f"📋 Running: pytest tests/ -v ...\n")
    result = subprocess.run(cmd)
    
    print(f"\n{SEPARATOR}")
    status = "✅ All tests passed!" if result.returncode == 0 else "❌ Some tests failed"
    print(status)
    print(SEPARATOR)
    
    return result.returncode


def generate_report() -> int:
    """Generate comprehensive test report"""
    print(f"\n{SEPARATOR}")
    print("📊 Generating Comprehensive Test Report")
    print(SEPARATOR)
    
    cmd = [sys.executable, "report-generators/generate-comprehensive-report.py"]
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\n{SEPARATOR}")
        print("✅ Report generated successfully!")
        print(f"📁 Location: {REPORT_DIR}/comprehensive-test-report.html")
        print(SEPARATOR)
    
    return result.returncode


def print_summary(test_result: int, report_result: int) -> None:
    """Print execution summary"""
    print(f"\n{SEPARATOR}")
    print("📋 TEST EXECUTION SUMMARY")
    print(SEPARATOR)
    print(f"✅ Test Results: {'PASSED' if test_result == 0 else 'FAILED'}")
    print(f"✅ Report Generation: {'SUCCESS' if report_result == 0 else 'FAILED'}")
    print()
    print("📁 Available Reports:")
    print(f"  • {REPORT_DIR}/detailed-report.html")
    print(f"  • {REPORT_DIR}/comprehensive-test-report.html")
    print(f"  • {LOG_DIR}/pytest.log")
    print(f"  • {LOG_DIR}/test_*.log")
    print(SEPARATOR)


def main() -> None:
    """Main entry point"""
    try:
        test_result = run_tests()
        report_result = generate_report()
        print_summary(test_result, report_result)
        sys.exit(test_result)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
