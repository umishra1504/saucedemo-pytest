from playwright.sync_api import Page
from utils.logger import get_logger


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CartPage")

        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.continue_shopping_btn = page.locator('[data-test="continue-shopping"]')
        self.checkout_btn = page.locator('[data-test="checkout"]')

    def get_cart_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        items = self.page.locator('[data-test="inventory-item-name"]')
        return [items.nth(i).text_content() for i in range(items.count())]

    def get_all_cart_item_names(self) -> list[str]:
        """Returns list of all product names in the cart."""
        return self.get_item_names()

    def get_item_price_by_name(self, product_name: str) -> str:
        """Returns the price of a specific product in the cart by its name."""
        items = self.page.locator('[data-test="inventory-item"]')
        for i in range(items.count()):
            item = items.nth(i)
            name_elem = item.locator('[data-test="inventory-item-name"]')
            if name_elem.text_content() == product_name:
                price_elem = item.locator('[data-test="inventory-item-price"]')
                return price_elem.text_content()
        return None

    def remove_item(self, index: int = 0):
        remove_buttons = self.page.locator('[data-test^="remove"]')
        remove_buttons.nth(index).click()
        self.log.info(f"Removed cart item at index {index}")

    def continue_shopping(self):
        self.continue_shopping_btn.click()
        self.log.info("Clicked continue shopping")

    def proceed_to_checkout(self):
        self.checkout_btn.click()
        self.log.info("Proceeded to checkout")
