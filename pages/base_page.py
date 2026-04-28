from playwright.sync_api import Page
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def navigate(self, path: str = ""):
        url = f"{self.page.context.browser.contexts[0]._impl_obj._browser.contexts[0]}"
        self.page.goto(path)
        self.log.info(f"Navigated to {path}")

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_element(self, selector: str, timeout: int = 10000):
        self.page.wait_for_selector(selector, timeout=timeout)
