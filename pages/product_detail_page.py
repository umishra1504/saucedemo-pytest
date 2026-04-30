from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    """Page object for SauceDemo product detail page."""

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("ProductDetailPage")

        self.back_button = page.locator('[data-test="back-to-products"]')
        self.product_name = page.locator('[data-test="inventory-item-name"]')
        self.product_description = page.locator('[data-test="inventory-item-desc"]')
        self.product_price = page.locator('[data-test="inventory-item-price"]')
        self.add_to_cart_button = page.locator('[data-test^="add-to-cart"]')
        self.remove_button = page.locator('[data-test^="remove"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def wait_for_loaded(self):
        self.product_name.wait_for(state="visible")
        self.product_description.wait_for(state="visible")
        self.product_price.wait_for(state="visible")
