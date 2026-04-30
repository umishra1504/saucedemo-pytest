from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutPage:
    """Page Object Model for SauceDemo Checkout Flow"""
    
    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutPage")

        # Step One - Information Form
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')

        # Step Two - Order Summary
        self.summary_items = page.locator('[data-test="inventory-item"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.back_btn = page.locator('[data-test="back-to-products"]')

        # Complete Page
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')
        self.back_home_btn = page.locator('[data-test="back-to-products"]')

    def is_on_step_one(self) -> bool:
        """Check if user is on checkout step one"""
        return self.STEP_ONE_URL in self.page.url

    def is_on_step_two(self) -> bool:
        """Check if user is on checkout step two"""
        return self.STEP_TWO_URL in self.page.url

    def is_on_complete_page(self) -> bool:
        """Check if user is on checkout complete page"""
        return self.COMPLETE_URL in self.page.url

    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill all shipping information fields"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.log.info(f"Filled shipping info: {first_name} {last_name}, {postal_code}")

    def click_continue(self):
        """Click continue button on step one"""
        self.continue_btn.click()
        self.log.info("Clicked continue button")

    def click_finish(self):
        """Click finish button on step two"""
        self.finish_btn.click()
        self.log.info("Clicked finish button")

    def click_cancel(self):
        """Click cancel button"""
        self.cancel_btn.click()
        self.log.info("Clicked cancel button")

    def get_error_message(self) -> str:
        """Get validation error message text"""
        if self.error_message.is_visible():
            return self.error_message.text_content()
        return ""

    def has_error(self) -> bool:
        """Check if error message is displayed"""
        return self.error_message.is_visible()

    def get_subtotal(self) -> str:
        """Get subtotal from order summary"""
        return self.subtotal_label.text_content()

    def get_tax(self) -> str:
        """Get tax from order summary"""
        return self.tax_label.text_content()

    def get_total(self) -> str:
        """Get total from order summary"""
        return self.total_label.text_content()

    def get_summary_item_count(self) -> int:
        """Get count of items in order summary"""
        return self.summary_items.count()

    def get_completion_header(self) -> str:
        """Get completion page header text"""
        return self.complete_header.text_content()

    def get_completion_text(self) -> str:
        """Get completion page confirmation text"""
        return self.complete_text.text_content()

    def is_first_name_field_visible(self) -> bool:
        """Check if first name field is visible"""
        return self.first_name_input.is_visible()

    def is_last_name_field_visible(self) -> bool:
        """Check if last name field is visible"""
        return self.last_name_input.is_visible()

    def is_postal_code_field_visible(self) -> bool:
        """Check if postal code field is visible"""
        return self.postal_code_input.is_visible()

    def get_first_name_value(self) -> str:
        """Get current value in first name field"""
        return self.first_name_input.input_value()

    def get_last_name_value(self) -> str:
        """Get current value in last name field"""
        return self.last_name_input.input_value()

    def get_postal_code_value(self) -> str:
        """Get current value in postal code field"""
        return self.postal_code_input.input_value()
