from playwright.sync_api import Page
from utils.logger import get_logger


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("InventoryPage")

        self.title = page.locator('[data-test="title"]')
        self.inventory_items = page.locator('[data-test="inventory-item"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def get_page_title(self) -> str:
        return self.title.text_content()

    def get_inventory_count(self) -> int:
        return self.inventory_items.count()

    def add_item_to_cart(self, index: int = 0):
        add_buttons = self.page.locator('[data-test^="add-to-cart"]')
        add_buttons.nth(index).click()
        self.log.info(f"Added item at index {index} to cart")

    def remove_item_from_cart(self, index: int = 0):
        remove_buttons = self.page.locator('[data-test^="remove"]')
        remove_buttons.nth(index).click()
        self.log.info(f"Removed item at index {index} from cart")

    def sort_by(self, value: str):
        self.sort_dropdown.select_option(value)
        self.log.info(f"Sorted inventory by: {value}")

    def get_item_names(self) -> list[str]:
        items = self.page.locator('[data-test="inventory-item-name"]')
        return [items.nth(i).text_content() for i in range(items.count())]

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        self.cart_link.click()
        self.log.info("Navigated to cart")
