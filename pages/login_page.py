from playwright.sync_api import Page
from utils.logger import get_logger
from utils.config import BASE_URL


class LoginPage:
    URL = BASE_URL

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("LoginPage")

        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def navigate(self):
        self.page.goto(self.URL)
        self.log.info("Navigated to login page")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.log.info(f"Login attempt with user: {username}")

    def get_error_message(self) -> str:
        return self.error_message.text_content()

    def is_error_displayed(self) -> bool:
        return self.error_message.is_visible()
