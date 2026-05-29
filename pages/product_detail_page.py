from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    """Page Object for SauceDemo product detail pages."""

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("ProductDetailPage")

        # Locators
        self.back_button = page.locator('[data-test="back-to-products"]')
        self.product_name = page.locator('[data-test="inventory-item-name"]')
        self.product_description = page.locator('[data-test="inventory-item-desc"]')
        self.product_price = page.locator('[data-test="inventory-item-price"]')
        self.add_to_cart_button = page.locator('[data-test^="add-to-cart"]')
        self.remove_button = page.locator('[data-test^="remove"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.product_image = page.locator('.inventory_details_img')

    def is_on_detail_page(self) -> bool:
        """Check if currently on a product detail page."""
        return "inventory-item.html" in self.page.url

    def get_product_name(self) -> str:
        """Get the product name displayed on the detail page."""
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        """Get the product description displayed on the detail page."""
        return self.product_description.text_content()

    def get_product_price(self) -> str:
        """Get the product price displayed on the detail page."""
        return self.product_price.text_content()

    def is_add_to_cart_visible(self) -> bool:
        """Check if Add to Cart button is visible."""
        return self.add_to_cart_button.is_visible()

    def is_product_name_visible(self) -> bool:
        """Check if product name is visible."""
        return self.product_name.is_visible()

    def is_product_description_visible(self) -> bool:
        """Check if product description is visible."""
        return self.product_description.is_visible()

    def is_product_price_visible(self) -> bool:
        """Check if product price is visible."""
        return self.product_price.is_visible()

    def add_to_cart(self):
        """Add the product to cart from detail page."""
        self.add_to_cart_button.click()
        self.log.info(f"Added product to cart from detail page")

    def remove_from_cart(self):
        """Remove the product from cart on detail page."""
        self.remove_button.click()
        self.log.info(f"Removed product from cart on detail page")

    def click_back_to_products(self):
        """Click the back button to return to inventory."""
        self.back_button.click()
        self.log.info("Clicked back to products button")

    def get_cart_badge_count(self) -> int:
        """Get the number displayed on the cart badge."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        """Navigate to cart page."""
        self.cart_link.click()
        self.log.info("Navigated to cart from product detail page")
