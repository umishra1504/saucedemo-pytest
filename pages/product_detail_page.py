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
        self.error_container = page.locator('[data-test="error"]')

    def open_from_inventory(self, index: int = 0):
        self.page.locator('[data-test="inventory-item-name"]').nth(index).click()
        self.log.info(f"Opened product detail page from inventory item {index}")

    def open_direct(self, product_id: str):
        self.page.goto(f"/inventory-item.html?id={product_id}")
        self.log.info(f"Opened product detail page directly for id={product_id}")

    def wait_for_loaded(self):
        self.product_name.wait_for(state="visible")
        self.product_description.wait_for(state="visible")
        self.product_price.wait_for(state="visible")

    def get_product_name(self) -> str:
        return self.product_name.text_content() or ""

    def get_product_description(self) -> str:
        return self.product_description.text_content() or ""

    def get_product_price(self) -> str:
        return self.product_price.text_content() or ""

    def add_to_cart(self):
        self.add_to_cart_button.click()
        self.log.info("Clicked Add to Cart on product detail page")

    def go_back_to_inventory(self):
        self.back_button.click()
        self.log.info("Returned to inventory from product detail page")

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content() or "0")
        return 0

    def is_add_to_cart_visible(self) -> bool:
        return self.add_to_cart_button.is_visible()

    def is_remove_visible(self) -> bool:
        return self.remove_button.is_visible()

    def has_error(self) -> bool:
        return self.error_container.is_visible()
