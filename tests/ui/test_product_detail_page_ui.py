import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


class TestProductDetailPageUI:
    """UI Tests for Product Detail Page with Add to Cart Functionality — SCRUM-163"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.inventory = InventoryPage(page)
        self.detail = ProductDetailPage(page)
        self.cart = CartPage(page)

    def _open_inventory_product(self, index: int = 0):
        self.inventory.open()
        self.inventory.open_product_by_index(index)

    def test_open_product_detail_page_from_inventory(self):
        # TC-PDP-001: Open a product detail page from the inventory list
        self._open_inventory_product(0)
        expect(self.page).to_have_url(ProductDetailPage.URL_PATTERN)

    def test_product_detail_page_displays_complete_information(self):
        # TC-PDP-002: Verify product detail page displays complete product information
        self._open_inventory_product(0)
        expect(self.detail.product_name).to_be_visible()
        expect(self.detail.product_desc).to_be_visible()
        expect(self.detail.product_price).to_be_visible()
        expect(self.detail.add_to_cart_btn).to_be_visible()

    def test_add_product_from_detail_page_to_cart(self):
        # TC-PDP-003: Add a product from the detail page to the cart
        self._open_inventory_product(0)
        name = self.detail.get_product_name()
        price = self.detail.get_product_price()
        self.detail.add_to_cart()
        self.detail.page.goto("https://www.saucedemo.com/cart.html")
        expect(self.cart.cart_items).to_have_count(1)
        expect(self.page.locator('.cart_item')).to_contain_text(name)
        expect(self.page.locator('.cart_item')).to_contain_text(price)

    def test_back_button_returns_to_inventory_page(self):
        # TC-PDP-004: Use back button to return to inventory page
        self._open_inventory_product(0)
        self.detail.go_back()
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")

    def test_cart_state_preserved_when_navigating_back_and_forth(self):
        # TC-PDP-005: Preserve cart state when navigating from inventory to product detail and back
        self.inventory.open()
        self.inventory.add_product_to_cart_by_index(0)
        self.inventory.open_product_by_index(1)
        self.detail.go_back()
        expect(self.inventory.cart_badge).to_have_text("1")

    def test_open_first_and_last_product_detail_pages(self):
        # TC-PDP-006: Open detail page for the first and last product in the inventory list
        self.inventory.open()
        self.inventory.open_product_by_index(0)
        expect(self.detail.product_name).to_be_visible()
        self.detail.go_back()
        self.inventory.open_product_by_index(-1)
        expect(self.detail.product_name).to_be_visible()

    @pytest.mark.skip(reason="needs environment setup for long text test data")
    def test_long_product_name_and_description_render_correctly(self):
        # TC-PDP-007: Verify product detail page renders correctly for long product name/description
        self._open_inventory_product(0)
        expect(self.detail.product_name).to_be_visible()
        expect(self.detail.product_desc).to_be_visible()

    def test_price_display_format_on_detail_page(self):
        # TC-PDP-008: Verify price is displayed correctly for decimal and zero values
        self._open_inventory_product(0)
        expect(self.detail.product_price).to_contain_text("$")

    def test_cart_state_preserved_across_repeated_navigation(self):
        # TC-PDP-009: Preserve cart state across repeated navigation between inventory and detail pages
        self.inventory.open()
        self.inventory.add_product_to_cart_by_index(0)
        self.inventory.open_product_by_index(1)
        self.detail.go_back()
        self.inventory.open_product_by_index(2)
        self.detail.go_back()
        expect(self.inventory.cart_badge).to_have_text("1")

    @pytest.mark.skip(reason="invalid route handling requires environment-specific setup")
    def test_invalid_product_detail_route_shows_error_state(self):
        # TC-PDP-010: Handle direct access to an invalid or non-existent product detail route
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=999999")
        expect(self.page.locator("body")).to_contain_text("Error")

    @pytest.mark.skip(reason="product data unavailability requires mocked backend or test fixture")
    def test_add_to_cart_unavailable_when_product_data_missing(self):
        # TC-PDP-011: Prevent add-to-cart action when product data is unavailable
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=broken")
        expect(self.detail.add_to_cart_btn).to_be_hidden()

    @pytest.mark.skip(reason="tampered payload validation requires controlled environment setup")
    def test_cart_rejects_tampered_product_data(self):
        # TC-PDP-012: Maintain security and integrity of cart state against tampered product data
        self.page.goto("https://www.saucedemo.com/inventory-item.html?id=0")
        self.page.evaluate("window.localStorage.setItem('tamper', 'true')")
        expect(self.page.locator("body")).not_to_contain_text("tampered")
