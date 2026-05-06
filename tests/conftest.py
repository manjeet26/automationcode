import pytest
import logging
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.logger import LoggerConfig, get_logger


# Store logs per test
test_logs = {}
current_test_logger = None


def pytest_configure(config):
    """Configure pytest with logging and directory setup"""
    Path("test-results").mkdir(exist_ok=True)
    Path("test-results/logs").mkdir(exist_ok=True)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Add file handler for all logs
    log_handler = logging.FileHandler("test-results/logs/all_tests.log")
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)


def pytest_runtest_setup(item):
    """Set up test-specific logger"""
    global current_test_logger
    test_name = item.name
    current_test_logger = LoggerConfig.setup_logging(test_name)
    current_test_logger.info(f"Starting test: {test_name}")
    item.test_logger = current_test_logger


def pytest_runtest_teardown(item):
    """Capture logs after test execution"""
    if hasattr(item, 'test_logger'):
        item.test_logger.info(f"Finished test: {item.name}")


@pytest.fixture
def logger(request):
    """Provide logger fixture to tests"""
    return request.node.test_logger if hasattr(request.node, 'test_logger') else get_logger(request.node.name)


@pytest.fixture
def login_page(page: Page, logger):
    """Fixture for login page with logging"""
    logger.info("Creating LoginPage instance")
    return LoginPage(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Set up browser context with proper viewport"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }
