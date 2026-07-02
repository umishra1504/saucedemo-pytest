from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutPage:
    URL_STEP_ONE = "https://www.saucedemo.com/checkout-step-one.html"
    URL_STEP_TWO = "https://www.saucedemo.com/checkout-step-two.html"
    URL_COMPLETE = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutPage")

        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.zip_code_input = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        self.error_container = page.locator('[data-test="error"]')
        self.summary_subtotal = page.locator('[data-test="subtotal-label"]')
        self.summary_tax = page.locator('[data-test="tax-label"]')
        self.summary_total = page.locator('[data-test="total-label"]')
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill_shipping_information(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_code_input.fill(zip_code)
        self.log.info("Filled shipping information")

    def continue_checkout(self):
        self.continue_btn.click()
        self.log.info("Clicked continue")

    def finish_checkout(self):
        self.finish_btn.click()
        self.log.info("Clicked finish")

    def get_error_message(self) -> str:
        return self.error_container.text_content() or ""

    def get_subtotal(self) -> str:
        return self.summary_subtotal.text_content() or ""

    def get_tax(self) -> str:
        return self.summary_tax.text_content() or ""

    def get_total(self) -> str:
        return self.summary_total.text_content() or ""

    def get_complete_header(self) -> str:
        return self.complete_header.text_content() or ""
