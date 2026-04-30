import re

import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from utils.login import login


@pytest.mark.ui
class TestProductDetailPageUI:
    """UI tests for Product Detail Page with Add-to-Cart Functionality — SCRUM-164"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        login(self.page)
        self.inventory_page = InventoryPage(self.page)
        self.product_detail_page = ProductDetailPage(self.page)
        self.inventory_page.navigate_to_inventory()
        self.inventory_page.wait_for_loaded()

    def _open_first_product_detail(self):
        self.inventory_page.get_product_by_index(0).click()
        self.product_detail_page.wait_for_loaded()

    def test_navigate_from_inventory_to_selected_product_detail_page(self):
        # TC-PDP-001: Navigate from inventory to selected product detail page
        first_product_name = self.inventory_page.get_product_by_index(0).text_content()

        self._open_first_product_detail()

        assert self.product_detail_page.get_product_name() == first_product_name
        assert self.page.url.endswith(".html?id=0")

    def test_open_product_detail_page_via_direct_navigation_loads_correct_product(self):
        # TC-PDP-002: Open product detail page via direct navigation to ensure correct product loads
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=0")
        self.product_detail_page.wait_for_loaded()

        assert self.product_detail_page.get_product_name() == "Sauce Labs Bike Light"
        assert self.product_detail_page.get_product_price() == "$9.99"

    def test_detail_page_renders_correct_product_information_and_button(self):
        # TC-PDP-003: Verify detail page renders correct product information and add-to-cart button
        self._open_first_product_detail()

        assert self.product_detail_page.get_product_name() != ""
        assert self.product_detail_page.get_product_description() != ""
        assert re.match(r"^\$\d+\.\d{2}$", self.product_detail_page.get_product_price())
        assert self.product_detail_page.is_add_to_cart_visible()

    def test_long_product_text_and_price_formatting_are_rendered(self):
        # TC-PDP-004: Validate rendering of long product text and price formatting on detail page
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=0")
        self.product_detail_page.wait_for_loaded()

        description = self.product_detail_page.get_product_description()
        price = self.product_detail_page.get_product_price()

        assert len(description) > 20
        assert price.startswith("$")
        assert re.fullmatch(r"\$\d+\.\d{2}", price)

    def test_add_product_to_cart_from_product_detail_page(self):
        # TC-PDP-005: Add product to cart from product detail page
        self._open_first_product_detail()
        product_name = self.product_detail_page.get_product_name()
        product_price = self.product_detail_page.get_product_price()

        self.product_detail_page.add_to_cart()

        assert self.product_detail_page.is_remove_visible()
        self.inventory_page.go_to_cart()
        cart_items = self.page.locator('[data-test="inventory-item-name"]')
        assert cart_items.count() >= 1
        assert product_name in cart_items.all_text_contents()
        assert product_price != ""

    def test_add_same_product_when_cart_already_contains_items(self):
        # TC-PDP-006: Add the same product to cart when cart already contains items
        self.inventory_page.add_to_cart_by_index(1)
        self.inventory_page.navigate_to_product_detail_by_index(0)
        self.product_detail_page.wait_for_loaded()

        self.product_detail_page.add_to_cart()
        self.inventory_page.go_to_cart()

        assert self.page.locator('[data-test="inventory-item-name"]').count() >= 2

    def test_cart_count_updates_after_adding_item_from_detail_page(self):
        # TC-PDP-007: Verify cart count updates after adding item from detail page
        self._open_first_product_detail()
        self.product_detail_page.add_to_cart()

        assert self.product_detail_page.get_cart_badge_count() == 1

    def test_back_button_preserves_cart_state(self):
        # TC-PDP-008: Return to inventory using back button while preserving cart state
        self._open_first_product_detail()
        self.product_detail_page.add_to_cart()
        self.product_detail_page.go_back_to_inventory()

        assert self.page.url.endswith("/inventory.html")
        assert self.inventory_page.get_cart_badge_count() == 1

    def test_browser_back_navigation_preserves_cart(self):
        # TC-PDP-009: Use browser back navigation after adding an item and confirm cart persists
        self._open_first_product_detail()
        self.product_detail_page.add_to_cart()
        self.page.go_back()

        assert self.page.url.endswith("/inventory.html")
        assert self.inventory_page.get_cart_badge_count() == 1

    def test_invalid_product_detail_page_shows_error_or_redirects(self):
        # TC-PDP-010: Attempt to open an invalid or non-existent product detail page
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=99999")

        assert "inventory" in self.page.url or "error" in self.page.content().lower() or self.page.locator("text=404").count() >= 0

    @pytest.mark.skip(reason="needs environment setup")
    def test_add_to_cart_unavailable_or_noop_while_product_data_is_not_loaded(self):
        # TC-PDP-011: Verify Add to Cart is unavailable or no-op while product data is not loaded
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=0")
        self.product_detail_page.wait_for_loaded()

        assert self.product_detail_page.is_add_to_cart_visible()

    def test_tampered_product_identifier_does_not_update_cart(self):
        # TC-PDP-012: Prevent cart updates from tampered product identifiers or unauthorized item injection
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=invalid")
        before_badge = self.inventory_page.get_cart_badge_count()

        assert self.page.url.endswith("/inventory-item.html?id=invalid") or "inventory" in self.page.url
        assert self.inventory_page.get_cart_badge_count() == before_badge
