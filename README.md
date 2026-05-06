# Admin Panel Test Automation

Professional test automation suite for admin panel with comprehensive logging and reporting.

![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)
![Version: 1.0](https://img.shields.io/badge/Version-1.0-blue)
![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue)

## Features

- **Advanced Logging System** - Multi-level logging (DEBUG to CRITICAL)
- **Professional HTML Reports** - Beautiful, interactive test reports
- **Automated Test Execution** - One-command test runs with reporting
- **Per-Test Logs** - Individual log files for each test
- **Centralized Logging** - Combined logs for all tests
- **CI/CD Ready** - Proper exit codes and automation
- **Zero Configuration** - Works out of the box

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests with Full Reporting
```bash
python scripts/run-tests-with-report.py
```

### View Reports
Reports are automatically generated in `test-results/`:
- `comprehensive-test-report.html` - Main test report with logs
- `detailed-report.html` - Pytest HTML report
- `sample-test-results.html` - Smoke test results summary

### Verify Setup
```bash
python scripts/verify-setup.py
```

## Project Structure

```
.
├── tests/                          # Test modules
│   ├── test_smoke.py              # Smoke tests (login, logout)
│   ├── test_login.py              # Login tests
│   ├── test_logout.py             # Logout tests
│   └── conftest.py                # Pytest fixtures and hooks
├── pages/                          # Page Object Model
│   ├── base_page.py               # Base page class
│   └── login_page.py              # Login page object
├── utils/                          # Utility modules
│   └── logger.py                  # Logging configuration
├── data/                           # Test data
│   └── config.json                # Configuration
├── scripts/                        # Runner and setup scripts
│   ├── run-tests-with-report.py   # Test runner with reporting
│   ├── run-tests.sh               # Interactive test menu
│   ├── run-sample-report.sh       # Sample report generator
│   ├── verify-setup.py            # Setup verification
│   ├── cleanup.sh                 # Project cleanup
│   └── setup-git.sh               # Git initialization
├── report-generators/              # Report generation tools
│   ├── generate-comprehensive-report.py  # Python HTML report
│   ├── generate-sample-report.py         # Sample report
│   ├── generate-html-report.js           # JS HTML report
│   └── generate-excel-report.js          # Excel report
├── playwright-js/                  # Playwright JS tests
│   ├── admin-panel-tests.spec.js  # JS test suite
│   ├── test-logout-popup.js       # Logout popup inspector
│   ├── inspect-logged-in.js       # Page inspection helper
│   └── inspect-page.js            # Page inspection helper
├── screenshots/                    # Test screenshots
├── docs/                           # Documentation
│   ├── START_HERE.md              # Quick start guide
│   ├── QUICK_REFERENCE.md         # Command reference
│   └── ...                        # Additional docs
├── test-results/                   # Generated reports and logs
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Testing

### Run All Tests
```bash
python scripts/run-tests-with-report.py
```

### Run Specific Test
```bash
pytest tests/test_smoke.py::test_smoke_admin_login_page_loads -v
```

### Run Smoke Tests Only
```bash
pytest -m smoke -v
```

### Run with Debug Logging
```bash
pytest tests/ -v --log-cli-level=DEBUG
```

## Logging

All test activities are logged at multiple levels:

| Level | Console | File | Use Case |
|-------|---------|------|----------|
| DEBUG | No | Yes | Detailed diagnostics |
| INFO | Yes | Yes | General information |
| WARNING | Yes | Yes | Potential issues |
| ERROR | Yes | Yes | Error events |
| CRITICAL | Yes | Yes | Critical errors |

**Log Locations:**
- Console: Real-time output during test run
- Files: `test-results/logs/`
  - `pytest.log` - Main pytest log
  - `all_tests.log` - Combined test logs
  - `test_*.log` - Individual test logs (per test)

## Using Logger in Tests

```python
def test_login(logger):
    logger.info("Test starting")
    # test code
    logger.info("Test passed")
```

The `logger` fixture is automatically available in all tests.

## Reports

HTML reports are generated automatically after tests run:

1. **Comprehensive Report** (`comprehensive-test-report.html`)
   - Test statistics and metrics
   - Expandable log sections
   - Beautiful responsive design

2. **Pytest Report** (`detailed-report.html`)
   - Test timeline
   - Pass/fail status with durations
   - Error tracebacks

3. **Sample Report** (`sample-test-results.html`)
   - Smoke test results summary
   - Generated from JSON test results

## Configuration

Edit `pytest.ini` to customize:

```ini
[pytest]
# Console logging level
--log-cli-level=INFO

# File logging level
--log-file-level=DEBUG

# Report output
--html=test-results/detailed-report.html

# Traceback format
--tb=short
```

## Command Reference

### Setup and Verification
```bash
python scripts/verify-setup.py          # Verify system setup
bash scripts/setup-git.sh               # Initialize git
```

### Test Execution
```bash
python scripts/run-tests-with-report.py # Run all tests with reports
pytest tests/ -v                        # Run tests with pytest
pytest -m smoke -v                      # Run smoke tests only
```

### Report Generation
```bash
python report-generators/generate-comprehensive-report.py  # Generate report
python report-generators/generate-sample-report.py         # Generate sample report
```

### View Logs
```bash
cat test-results/logs/pytest.log        # View main log
cat test-results/logs/test_*.log        # View specific test log
```

## CI/CD Integration

The system is ready for CI/CD pipelines:

```bash
#!/bin/bash
python scripts/run-tests-with-report.py
if [ $? -eq 0 ]; then
    echo "Tests passed"
else
    echo "Tests failed"
    exit 1
fi
```

## Troubleshooting

### Tests Won't Run
```bash
python scripts/verify-setup.py
pip install -r requirements.txt
```

### Logger Not Available
```python
def test_example(logger):  # Add logger parameter
    logger.info("message")
```

## Best Practices

1. **Log Important Steps**
   ```python
   logger.info("Navigating to login page")
   logger.info("Entering credentials")
   logger.info("Test passed")
   ```

2. **Use Appropriate Log Levels**
   - `debug()` for detailed diagnostics
   - `info()` for general flow
   - `warning()` for potential issues
   - `error()` for failures

3. **Keep Logs Clean**
   - Old logs are timestamped automatically
   - Archive periodically
   - Don't commit logs to git

## Documentation

- **docs/START_HERE.md** - 5-minute quick start guide
- **docs/QUICK_REFERENCE.md** - Commands and troubleshooting
- **docs/LOGGING_AND_REPORTING.md** - Complete feature guide

## License

Internal - All Rights Reserved

---

**Version:** 1.0
**Status:** Production Ready
**Last Updated:** May 6, 2026
