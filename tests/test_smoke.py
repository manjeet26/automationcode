import os
import logging

import pytest
from playwright.sync_api import Page, expect


ADMIN_URL = os.getenv("ADMIN_PANEL_URL", "https://adminauctionqa.gaadi.com")
ADMIN_USERNAME = os.getenv("ADMIN_PANEL_USERNAME", "administrator")
ADMIN_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "testing")
INVALID_PASSWORD = os.getenv("ADMIN_PANEL_INVALID_PASSWORD", "testing@123")

USERNAME_INPUT = 'input[name="username"].sign-txtbox'
PASSWORD_INPUT = 'input[name="password"].sign-txtbox'
SIGN_IN_BUTTON = 'button:has-text("SIGN IN")'
MANAGE_AUCTION_URL_PATTERN = "**/auction/manageAuction**"

logger = logging.getLogger(__name__)


def open_admin_login(page: Page, logger: logging.Logger) -> None:
    logger.info(f"Navigating to admin panel: {ADMIN_URL}")
    page.goto(ADMIN_URL, wait_until="networkidle", timeout=30000)
    logger.info("Waiting for username input to be visible")
    expect(page.locator(USERNAME_INPUT)).to_be_visible(timeout=10000)
    logger.info("Admin login page loaded successfully")


def login_to_admin(page: Page, password: str = ADMIN_PASSWORD, logger: logging.Logger = None) -> None:
    if logger is None:
        logger = logging.getLogger(__name__)
    logger.info(f"Attempting login with username: {ADMIN_USERNAME}")
    page.fill(USERNAME_INPUT, ADMIN_USERNAME)
    page.fill(PASSWORD_INPUT, password)
    logger.info("Clicking SIGN IN button")
    page.click(SIGN_IN_BUTTON)


@pytest.mark.smoke
def test_smoke_admin_login_page_loads(page: Page, logger):
    logger.info("Test: Verify admin login page loads")
    open_admin_login(page, logger)

    logger.info("Verifying username input is visible")
    expect(page.locator(USERNAME_INPUT)).to_be_visible()
    logger.info("Verifying password input is visible")
    expect(page.locator(PASSWORD_INPUT)).to_be_visible()
    logger.info("Verifying SIGN IN button is visible")
    expect(page.locator(SIGN_IN_BUTTON)).to_be_visible()
    logger.info("✅ Test passed: All login elements are visible")


@pytest.mark.smoke
def test_smoke_admin_login_with_valid_credentials(page: Page, logger):
    logger.info("Test: Verify admin login with valid credentials")
    open_admin_login(page, logger)
    login_to_admin(page, logger=logger)

    logger.info("Waiting for URL change to manage auction page")
    page.wait_for_url(MANAGE_AUCTION_URL_PATTERN, timeout=15000)
    logger.info(f"Current URL: {page.url}")
    assert "/auction/manageAuction" in page.url
    logger.info("✅ Test passed: User successfully logged in")


@pytest.mark.smoke
def test_smoke_admin_login_with_invalid_credentials_is_blocked(page: Page, logger):
    logger.info("Test: Verify login is blocked with invalid credentials")
    logger.warning(f"Using invalid password: {INVALID_PASSWORD}")
    open_admin_login(page, logger)
    login_to_admin(page, password=INVALID_PASSWORD, logger=logger)

    logger.info("Waiting for login attempt to complete")
    page.wait_for_timeout(2000)
    logger.info(f"Current URL after invalid login: {page.url}")
    assert "/auction/manageAuction" not in page.url
    logger.info("✅ Test passed: Invalid login was blocked")


@pytest.mark.smoke
def test_smoke_admin_logout(page: Page, logger):
    logger.info("Test: Verify admin logout functionality")
    open_admin_login(page, logger)
    login_to_admin(page, logger=logger)
    logger.info("Waiting for URL change to manage auction page")
    page.wait_for_url(MANAGE_AUCTION_URL_PATTERN, timeout=15000)

    logger.info("Setting up dialog handler for logout confirmation")
    page.on("dialog", lambda dialog: dialog.accept())
    logger.info("Executing JavaScript to open dropdown menu")
    page.evaluate(
        """
        () => {
            const dropdown = document.querySelector('.login-btn-mob');
            if (!dropdown) return;
            dropdown.classList.add('open');
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) menu.style.display = 'block';
        }
        """
    )
    logger.info("Clicking logout button")
    page.locator(".login-btn-mob .confirm_logout").click(force=True)
    page.wait_for_timeout(3000)

    logger.info(f"Current URL after logout: {page.url}")
    assert "/auction/manageAuction" not in page.url
    logger.info("Verifying user is back on login page")
    expect(page.locator(USERNAME_INPUT)).to_be_visible(timeout=15000)
    logger.info("✅ Test passed: User successfully logged out")
