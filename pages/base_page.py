from playwright.sync_api import Page, Response

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> Response:
        return self.page.goto(url)

    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)

    def click(self, selector: str):
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        self.page.fill(selector, value)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
