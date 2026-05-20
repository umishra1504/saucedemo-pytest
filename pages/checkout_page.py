from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutPage:
    """Page Object for Checkout Step One - Shipping Information"""
    
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutPage")

        # Shipping form fields
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.zip_code_input = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
        """Fill all shipping information fields"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_code_input.fill(zip_code)
        self.log.info(f"Filled shipping info: {first_name} {last_name}, {zip_code}")

    def click_continue(self):
        """Click continue button to proceed to order summary"""
        self.continue_btn.click()
        self.log.info("Clicked continue button")

    def click_cancel(self):
        """Cancel checkout and return to cart"""
        self.cancel_btn.click()
        self.log.info("Cancelled checkout")

    def get_error_message(self) -> str:
        """Get validation error message text"""
        return self.error_message.text_content()

    def is_error_displayed(self) -> bool:
        """Check if validation error is visible"""
        return self.error_message.is_visible()

    def is_on_checkout_page(self) -> bool:
        """Verify user is on checkout step one page"""
        return "checkout-step-one" in self.page.url
