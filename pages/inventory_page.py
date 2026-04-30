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
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_descriptions = page.locator('[data-test="inventory-item-desc"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.item_link = page.locator('[data-test="inventory-item-name"]')
        self.add_buttons = page.locator('[data-test^="add-to-cart"]')

    def navigate_to_inventory(self):
        self.page.goto(self.URL)
        self.log.info("Navigated to inventory page")

    def wait_for_loaded(self):
        self.title.wait_for(state="visible")
        self.inventory_items.first.wait_for(state="visible")

    def get_page_title(self) -> str:
        return self.title.text_content() or ""

    def get_inventory_count(self) -> int:
        return self.inventory_items.count()

    def get_product_by_index(self, index: int = 0):
        return self.item_link.nth(index)

    def navigate_to_product_detail_by_index(self, index: int = 0):
        self.get_product_by_index(index).click()
        self.log.info(f"Opened product detail page for index {index}")

    def get_product_name_by_index(self, index: int = 0) -> str:
        return self.item_names.nth(index).text_content() or ""

    def get_product_description_by_index(self, index: int = 0) -> str:
        return self.item_descriptions.nth(index).text_content() or ""

    def get_product_price_by_index(self, index: int = 0) -> str:
        return self.item_prices.nth(index).text_content() or ""

    def add_item_to_cart(self, index: int = 0):
        self.add_buttons.nth(index).click()
        self.log.info(f"Added item at index {index} to cart")

    def remove_item_from_cart(self, index: int = 0):
        remove_buttons = self.page.locator('[data-test^="remove"]')
        remove_buttons.nth(index).click()
        self.log.info(f"Removed item at index {index} from cart")

    def sort_by(self, value: str):
        self.sort_dropdown.select_option(value)
        self.log.info(f"Sorted inventory by: {value}")

    def get_item_names(self) -> list[str]:
        return [self.item_names.nth(i).text_content() or "" for i in range(self.item_names.count())]

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content() or "0")
        return 0

    def go_to_cart(self):
        self.cart_link.click()
        self.log.info("Navigated to cart")
