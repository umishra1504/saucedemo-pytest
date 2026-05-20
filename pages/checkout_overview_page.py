from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutOverviewPage:
    """Page Object for Checkout Step Two - Order Summary/Overview"""

    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutOverviewPage")

        # Order summary elements
        self.item_total_label = page.locator('.summary_subtotal_label')
        self.tax_label = page.locator('.summary_tax_label')
        self.total_label = page.locator('.summary_total_label')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        
        # Cart items in summary
        self.cart_items = page.locator('.cart_item')

    def get_item_total(self) -> float:
        """Extract item subtotal from summary"""
        text = self.item_total_label.text_content()
        # Extract numeric value from "Item total: $XX.XX"
        amount = text.split('$')[1]
        return float(amount)

    def get_tax(self) -> float:
        """Extract tax amount from summary"""
        text = self.tax_label.text_content()
        # Extract numeric value from "Tax: $X.XX"
        amount = text.split('$')[1]
        return float(amount)

    def get_total(self) -> float:
        """Extract total amount from summary"""
        text = self.total_label.text_content()
        # Extract numeric value from "Total: $XX.XX"
        amount = text.split('$')[1]
        return float(amount)

    def is_item_total_displayed(self) -> bool:
        """Verify item total is visible"""
        return self.item_total_label.is_visible()

    def is_tax_displayed(self) -> bool:
        """Verify tax is visible"""
        return self.tax_label.is_visible()

    def click_finish(self):
        """Complete the purchase"""
        self.finish_btn.click()
        self.log.info("Clicked finish button to complete purchase")

    def click_cancel(self):
        """Cancel and return to products"""
        self.cancel_btn.click()
        self.log.info("Cancelled order")

    def get_cart_item_count(self) -> int:
        """Get number of items in order summary"""
        return self.cart_items.count()

    def is_on_overview_page(self) -> bool:
        """Verify user is on checkout overview page"""
        return "checkout-step-two" in self.page.url
