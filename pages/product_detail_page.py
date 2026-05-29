from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    """Page object for product detail page (inventory-item.html)."""

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
        """Returns the product name displayed on the detail page."""
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        """Returns the product description."""
        return self.product_description.text_content()

    def get_product_price(self) -> str:
        """Returns the product price (e.g., '$29.99')."""
        return self.product_price.text_content()

    def is_add_to_cart_button_visible(self) -> bool:
        """Checks if Add to Cart button is visible."""
        return self.add_to_cart_btn.is_visible()

    def add_to_cart(self):
        """Clicks the Add to Cart button on the product detail page."""
        self.add_to_cart_btn.click()
        self.log.info(f"Added product to cart from detail page")

    def remove_from_cart(self):
        """Clicks the Remove button on the product detail page."""
        self.remove_btn.click()
        self.log.info(f"Removed product from cart on detail page")

    def is_remove_button_visible(self) -> bool:
        """Checks if Remove button is visible (product is in cart)."""
        return self.remove_btn.is_visible()

    def back_to_products(self):
        """Clicks the back to products button."""
        self.back_to_products_btn.click()
        self.log.info("Navigated back to products")

    def get_cart_badge_count(self) -> int:
        """Returns the number displayed in the cart badge, or 0 if not visible."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        """Navigates to the shopping cart."""
        self.cart_link.click()
        self.log.info("Navigated to cart from detail page")

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.page.url
