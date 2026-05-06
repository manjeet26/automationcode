import os
import logging

import pytest
from playwright.sync_api import Page, expect


ADMIN_URL = os.getenv("ADMIN_PANEL_URL", "https://adminauctionqa.gaadi.com")
ADMIN_USERNAME = os.getenv("ADMIN_PANEL_USERNAME", "administrator")
ADMIN_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "testing")

USERNAME_INPUT = 'input[name="username"].sign-txtbox'
PASSWORD_INPUT = 'input[name="password"].sign-txtbox'
SIGN_IN_BUTTON = 'button:has-text("SIGN IN")'
MANAGE_AUCTION_URL_PATTERN = "**/auction/manageAuction**"

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.logout
def test_logout_functionality(page: Page, logger):
    """Test case: Verify admin user can successfully logout from the admin panel"""
    logger.info("Test: Verify admin logout functionality")

    logger.info(f"Navigating to admin panel: {ADMIN_URL}")
    page.goto(ADMIN_URL, wait_until="networkidle", timeout=30000)
    expect(page.locator(USERNAME_INPUT)).to_be_visible(timeout=10000)
    logger.info("Admin login page loaded successfully")

    logger.info(f"Attempting login with username: {ADMIN_USERNAME}")
    page.fill(USERNAME_INPUT, ADMIN_USERNAME)
    page.fill(PASSWORD_INPUT, ADMIN_PASSWORD)
    logger.info("Clicking SIGN IN button")
    page.click(SIGN_IN_BUTTON)

    logger.info("Waiting for URL change to manage auction page")
    page.wait_for_url(MANAGE_AUCTION_URL_PATTERN, timeout=15000)
    logger.info(f"Current URL after login: {page.url}")
    assert "/auction/manageAuction" in page.url
    logger.info("User successfully logged in")

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
    logger.info("Test passed: User successfully logged out")
