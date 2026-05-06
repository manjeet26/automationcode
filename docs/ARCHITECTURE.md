# Logging & Reporting Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Test Execution Flow                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   pytest runs    │
                    │  (pytest.ini)    │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │Test Setup│    │Test Run  │    │Test Tear│
      │conftest  │    │test_*.py │    │ down    │
      └────┬─────┘    └────┬─────┘    └────┬────┘
           │               │              │
           ▼               ▼              ▼
    ┌─────────────────────────────────────────┐
    │     Test-Specific Logger Created        │
    │  (LoggerConfig.setup_logging())         │
    │     with 2 Handlers                     │
    └──────────┬──────────────────┬───────────┘
               │                  │
        ┌──────▼──────┐    ┌──────▼──────┐
        │   Console   │    │  File (*.log)│
        │  INFO+      │    │  DEBUG+      │
        └─────────────┘    └──────┬───────┘
                                  │
                                  ▼
                     ┌──────────────────────┐
                     │ test-results/logs/   │
                     │ ├─ pytest.log        │
                     │ ├─ all_tests.log     │
                     │ └─ test_*.log        │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Report Generators    │
                     │ ├─ pytest-html       │
                     │ └─ custom report     │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ test-results/        │
                     │ ├─ detailed-report   │
                     │ └─ comprehensive-rep │
                     └──────────────────────┘
```

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                          Test Execution                             │
└────────────────────────────────────────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
          ┌──────────┐       ┌──────────┐     ┌──────────┐
          │pytest.ini│       │conftest  │     │test_*.py │
          │          │       │          │     │          │
          │Logging   │       │Logger    │     │Tests with│
          │Config    │       │setup     │     │logger    │
          └────┬─────┘       └────┬─────┘     └────┬─────┘
               │                  │                │
               └──────────┬───────┴────────┬───────┘
                          │                │
                    ┌─────▼────────────────▼─────┐
                    │  utils/logger.py           │
                    │  LoggerConfig class        │
                    │                            │
                    │  • setup_logging()         │
                    │  • get_logger()            │
                    │  • Formatting              │
                    │  • File/Console handlers   │
                    └─────┬────────────────┬─────┘
                          │                │
              ┌───────────┴┴───────────┐   │
              │                       │   │
              ▼                       ▼   ▼
        ┌──────────────┐      ┌────────────────┐
        │Console Output│      │Log Files in    │
        │(INFO+)       │      │test-results/   │
        │              │      │logs/           │
        │• Navigation  │      │                │
        │• Login steps │      │• pytest.log    │
        │• Assertions  │      │• all_tests.log │
        │• Status      │      │• test_*.log    │
        └──────────────┘      └────────┬───────┘
                                       │
                      ┌────────────────┴────────────────┐
                      │                                 │
                      ▼                                 ▼
            ┌──────────────────┐            ┌──────────────────┐
            │generate-          │            │pytest-html       │
            │comprehensive-    │            │report plugin     │
            │report.py         │            │                  │
            │                  │            │                  │
            │• Parse logs      │            │• Auto-generated  │
            │• Extract data    │            │• Pass/fail info  │
            │• Build HTML      │            │• Durations       │
            │• Styling         │            │• Tracebacks      │
            └────────┬─────────┘            └────────┬─────────┘
                     │                               │
                     └────────────┬──────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   test-results/            │
                    │   ├─ detailed-report.html  │
                    │   ├─ comprehensive-        │
                    │   │  test-report.html      │
                    │   └─ smoke-test-report.html│
                    └────────────────────────────┘
```

## Data Flow Diagram

```
Tests Running
    │
    ├──► Logger.info("Test step")
    │    └──► Formatted Message
    │         ├──► Console Output (INFO+)
    │         │    └──► User sees real-time progress
    │         │
    │         └──► File Output (DEBUG+)
    │              └──► test-results/logs/
    │                   ├─ pytest.log (root)
    │                   ├─ all_tests.log (combined)
    │                   └─ test_name_*.log (per-test)
    │
    └──► Test Completes
         │
         ├──► Logs collected from:
         │    ├─ pytest.log
         │    ├─ all_tests.log
         │    └─ test_*.log files
         │
         └──► Report Generation
              │
              ├──► Comprehensive Report
              │    ├─ Parse test logs
              │    ├─ Extract stats
              │    ├─ Build HTML
              │    └─► comprehensive-test-report.html
              │
              └──► Pytest HTML Report
                   ├─ pytest-html plugin
                   └─► detailed-report.html
```

## File Organization

```
adminPanelWebAutomation/
│
├── utils/
│   └── logger.py ..................... Logger configuration class
│       ├── LoggerConfig.setup_logging()
│       └── get_logger()
│
├── tests/
│   ├── conftest.py ................... Test configuration
│   │   ├── pytest_configure() ........ Setup pytest
│   │   ├── pytest_runtest_setup() .... Per-test logger
│   │   └── @pytest.fixture logger ... Logger injection
│   │
│   ├── test_smoke.py ................. Tests with logging
│   │   └── Uses logger fixture
│   │
│   └── test_login.py
│
├── pytest.ini ........................ Logging configuration
│   ├── --log-cli=true
│   ├── --log-file=...
│   └── --log-file-level=DEBUG
│
├── run-tests-with-report.py .......... Automated runner
│   ├── Run pytest
│   └── Generate reports
│
├── generate-comprehensive-report.py . Report generator
│   ├── Parse logs
│   ├── Extract stats
│   └── Generate HTML
│
├── run-tests.sh ...................... Interactive menu
│
├── requirements.txt .................. Dependencies
│   ├── pytest
│   ├── pytest-html
│   └── pytest-playwright
│
└── test-results/
    ├── logs/ ......................... Log storage
    │   ├── pytest.log ................ Main pytest log
    │   ├── all_tests.log ............. Combined logs
    │   └── test_*.log ................ Per-test logs
    │
    ├── comprehensive-test-report.html . Custom report
    ├── detailed-report.html ........... Pytest report
    └── smoke-test-report.html ......... Legacy report
```

## Log Levels and Handlers

```
┌─────────────────────────────────────────────────────────────┐
│                  Log Level Hierarchy                        │
│                  (Higher = More Severe)                     │
└─────────────────────────────────────────────────────────────┘

CRITICAL  ──┐
            │
ERROR     ──┼──► File Handler (DEBUG+) ──► *.log files
            │    ├─ Detailed formatting
WARNING   ──┼──► ├─ Timestamp
            │    ├─ File:Line
INFO      ──┤    ├─ Function name
            │    └─ Full context
DEBUG     ──┘
            
            Console Handler (INFO+)
            ├─ Simple formatting
            ├─ Level - Message
            └─ User readable
```

## Report Generation Pipeline

```
Step 1: Tests Execute
    ↓
Step 2: Logs Written to Files
    ├─ Console handler outputs
    └─ File handlers write logs
    ↓
Step 3: Log Files Exist
    ├─ test-results/logs/pytest.log
    ├─ test-results/logs/all_tests.log
    └─ test-results/logs/test_*.log
    ↓
Step 4: Report Generation
    ├─ generate-comprehensive-report.py
    │  ├─ Read all log files
    │  ├─ Parse pytest output
    │  ├─ Extract test stats
    │  └─ Build HTML report
    │
    └─ pytest-html plugin
       ├─ Auto-generated
       ├─ Test timeline
       └─ Pass/fail status
    ↓
Step 5: Reports Generated
    ├─ test-results/comprehensive-test-report.html
    ├─ test-results/detailed-report.html
    └─ test-results/smoke-test-report.html
    ↓
Step 6: View in Browser
    Open in any web browser
```

## Integration Points

```
Integration with Pytest:
    pytest.ini
        ↓
    conftest.py (pytest_configure)
        ↓
    Root logger setup
        ↓
    Each test run
        ↓
    conftest.py (pytest_runtest_setup)
        ↓
    Test-specific logger created
        ↓
    Test logger injected via fixture
        ↓
    Test executes with logging
        ↓
    Logs written to files
        ↓
    conftest.py (pytest_runtest_teardown)
        ↓
    Test completes

Integration with Playwright:
    page.goto() ──► Logger: "Navigating..."
    page.fill() ──► Logger: "Filling input..."
    page.click() ──► Logger: "Clicking element..."
    expect() ────► Logger: "Asserting..."
```

## Execution Timeline

```
Timeline of a Test Run:

T+0s    │ pytest starts
        │ pytest_configure() called
        │ Create test-results/logs directory
        │
T+1s    │ Test 1 starts
        │ pytest_runtest_setup() called
        │ Create test-specific logger
        │ logger.info("Starting test")
        │
T+2s    │ Test executes
        │ logger.info("Navigating...")
        │ page.goto(url)
        │ logger.info("Clicking...")
        │ page.click(selector)
        │
T+5s    │ Test completes
        │ logger.info("Test passed")
        │ pytest_runtest_teardown() called
        │
T+6s    │ Test 2 starts
        │ (repeat for each test)
        │
T+15s   │ All tests completed
        │ Logs written to files:
        │ ├─ test-results/logs/pytest.log
        │ ├─ test-results/logs/all_tests.log
        │ └─ test-results/logs/test_*.log
        │
T+16s   │ generate-comprehensive-report.py
        │ ├─ Read all log files
        │ ├─ Parse pytest output
        │ ├─ Generate HTML
        │ └─ Save report
        │
T+17s   │ Reports ready:
        │ ├─ detailed-report.html (pytest)
        │ └─ comprehensive-test-report.html
        │
T+18s   │ Complete!
        │ User can view reports
```

---

This architecture ensures:
- ✅ Comprehensive logging at all levels
- ✅ Real-time console feedback
- ✅ Detailed file logs for analysis
- ✅ Professional HTML reports
- ✅ Easy debugging and troubleshooting
- ✅ CI/CD integration ready
