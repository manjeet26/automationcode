import pytest
from pages.login_page import LoginPage

def test_login_page_loads(login_page: LoginPage):
    # Using a public test site for initial verification
    login_page.navigate("https://practicetestautomation.com/practice-test-login/")
    assert login_page.is_visible("input[name='username']")

def test_invalid_login(login_page: LoginPage):
    login_page.navigate("https://practicetestautomation.com/practice-test-login/")
    # These selectors happen to match the practice site
    login_page.login("incorrect_user", "incorrect_password")
    # Note: Selectors in LoginPage might need adjustment for specific sites
    # This is a placeholder for the verification logic
    # assert login_page.is_visible("#error")
