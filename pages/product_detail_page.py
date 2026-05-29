from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    """Page Object for Product Detail Page"""

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("ProductDetailPage")

        # Locators
        self.product_name = page.locator('[data-test="inventory-item-name"]')
        self.product_description = page.locator('[data-test="inventory-item-desc"]')
        self.product_price = page.locator('[data-test="inventory-item-price"]')
        self.add_to_cart_btn = page.locator('[data-test^="add-to-cart"]')
        self.remove_btn = page.locator('[data-test^="remove"]')
        self.back_to_products_btn = page.locator('[data-test="back-to-products"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def get_product_name(self) -> str:
        """Get the displayed product name."""
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        """Get the displayed product description."""
        return self.product_description.text_content()

    def get_product_price(self) -> str:
        """Get the displayed product price."""
        return self.product_price.text_content()

    def is_add_to_cart_visible(self) -> bool:
        """Check if Add to Cart button is visible."""
        return self.add_to_cart_btn.is_visible()

    def is_product_detail_displayed(self) -> bool:
        """Verify all product detail elements are visible."""
        return (
            self.product_name.is_visible()
            and self.product_description.is_visible()
            and self.product_price.is_visible()
            and self.add_to_cart_btn.is_visible()
        )

    def add_to_cart(self):
        """Add the product to cart from detail page."""
        product_name = self.get_product_name()
        self.add_to_cart_btn.click()
        self.log.info(f"Added '{product_name}' to cart from detail page")

    def is_remove_button_visible(self) -> bool:
        """Check if Remove button is visible (product is in cart)."""
        return self.remove_btn.is_visible()

    def go_back_to_inventory(self):
        """Click the back button to return to inventory."""
        self.back_to_products_btn.click()
        self.log.info("Navigated back to inventory page")

    def get_cart_badge_count(self) -> int:
        """Get the cart badge count."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        """Navigate to cart page."""
        self.cart_link.click()
        self.log.info("Navigated to cart from product detail page")
