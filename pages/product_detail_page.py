from playwright.sync_api import Page
from utils.logger import get_logger


class ProductDetailPage:
    URL_PATTERN = "https://www.saucedemo.com/inventory-item.html?id=*"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("ProductDetailPage")

        self.back_button = page.locator('[data-test="back-to-products"]')
        self.product_name = page.locator('[data-test="inventory-item-name"]')
        self.product_desc = page.locator('[data-test="inventory-item-desc"]')
        self.product_price = page.locator('[data-test="inventory-item-price"]')
        self.add_to_cart_btn = page.locator('[data-test^="add-to-cart"]')
        self.remove_btn = page.locator('[data-test^="remove"]')

    def get_product_name(self) -> str:
        return self.product_name.text_content()

    def get_product_description(self) -> str:
        return self.product_desc.text_content()

    def get_product_price(self) -> str:
        return self.product_price.text_content()

    def is_add_to_cart_visible(self) -> bool:
        return self.add_to_cart_btn.is_visible()

    def add_to_cart(self):
        self.add_to_cart_btn.click()
        self.log.info("Clicked add to cart on product detail page")

    def go_back(self):
        self.back_button.click()
        self.log.info("Clicked back from product detail page")
