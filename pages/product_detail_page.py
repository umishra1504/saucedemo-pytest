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

    def open_from_inventory(self, product_index: int = 0):
        item_titles = self.page.locator('[data-test="inventory-item-name"]')
        item_titles.nth(product_index).click()
        self.log.info(f"Opened product detail page for inventory item at index {product_index}")

    def navigate_directly(self, product_slug: str):
        self.page.goto(f"https://www.saucedemo.com/inventory-item.html?id={product_slug}")
        self.log.info(f"Navigated directly to product detail page with slug {product_slug}")

    def get_product_name(self) -> str:
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        return self.product_description.text_content()

    def get_product_price(self) -> str:
        return self.product_price.text_content()

    def add_to_cart(self):
        self.add_to_cart_button.click()
        self.log.info("Clicked Add to Cart on product detail page")

    def go_back_to_inventory(self):
        self.back_button.click()
        self.log.info("Clicked back to products")

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0
