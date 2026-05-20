from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutCompletePage:
    """Page Object for Checkout Complete - Purchase Confirmation"""

    URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutCompletePage")

        # Confirmation elements
        self.complete_header = page.locator('.complete-header')
        self.complete_text = page.locator('.complete-text')
        self.back_home_btn = page.locator('[data-test="back-to-products"]')

    def is_order_complete(self) -> bool:
        """Verify order completion page is displayed"""
        return self.complete_header.is_visible() and "checkout-complete" in self.page.url

    def get_confirmation_header(self) -> str:
        """Get confirmation header text"""
        return self.complete_header.text_content()

    def get_confirmation_text(self) -> str:
        """Get confirmation message text"""
        return self.complete_text.text_content()

    def click_back_home(self):
        """Navigate back to products page"""
        self.back_home_btn.click()
        self.log.info("Clicked back to products")
