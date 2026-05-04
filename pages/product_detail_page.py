from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    """Page Object for Product Detail Page - SCRUM-167"""

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
        """Get the product name displayed on detail page"""
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        """Get the product description displayed on detail page"""
        return self.product_description.text_content()

    def get_product_price(self) -> str:
        """Get the product price displayed on detail page"""
        return self.product_price.text_content()

    def is_add_to_cart_visible(self) -> bool:
        """Check if Add to Cart button is visible"""
        return self.add_to_cart_btn.is_visible()

    def add_to_cart(self):
        """Click Add to Cart button"""
        self.add_to_cart_btn.click()
        self.log.info("Clicked Add to Cart on product detail page")

    def is_remove_button_visible(self) -> bool:
        """Check if Remove button is visible (indicates item is in cart)"""
        return self.remove_btn.is_visible()

    def click_back_to_products(self):
        """Click back to products button"""
        self.back_to_products_btn.click()
        self.log.info("Clicked back to products")

    def navigate_back(self):
        """Use browser back button"""
        self.page.go_back()
        self.log.info("Used browser back button")

    def get_cart_badge_count(self) -> int:
        """Get the cart badge count"""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        """Navigate to cart page"""
        self.cart_link.click()
        self.log.info("Navigated to cart from product detail page")

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
