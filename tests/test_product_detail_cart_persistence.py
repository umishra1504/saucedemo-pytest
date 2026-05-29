import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


class TestProductDetailCartPersistence:
    """UI Tests for Product detail page from inventory with cart persistence — SCRUM-176"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Login and navigate to inventory before each test."""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        
        self.inventory_page = InventoryPage(page)
        self.product_detail_page = ProductDetailPage(page)
        self.cart_page = CartPage(page)
        self.page = page

    def test_open_product_detail_from_inventory(self):
        """TC-FP-001: Open a product detail page from the inventory list"""
        # Get first product name from inventory
        product_names = self.inventory_page.get_all_product_names()
        assert len(product_names) > 0, "No products found in inventory"
        
        first_product = product_names[0]
        
        # Click on the product to open detail page
        self.inventory_page.click_product_by_name(first_product)
        
        # Verify we're on a product detail page
        assert "inventory-item.html" in self.product_detail_page.get_current_url()
        
        # Verify the product name matches
        detail_product_name = self.product_detail_page.get_product_name()
        assert detail_product_name == first_product

    def test_verify_product_details_and_add_to_cart_button(self):
        """TC-FP-002: Verify product details and Add to Cart button render on the detail page"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        self.inventory_page.click_product_by_name(product_names[0])
        
        # Verify product name is displayed
        product_name = self.product_detail_page.get_product_name()
        assert product_name is not None and len(product_name) > 0
        
        # Verify product description is displayed
        product_desc = self.product_detail_page.get_product_description()
        assert product_desc is not None and len(product_desc) > 0
        
        # Verify product price is displayed and formatted correctly
        product_price = self.product_detail_page.get_product_price()
        assert product_price.startswith("$")
        
        # Verify Add to Cart button is visible
        assert self.product_detail_page.is_add_to_cart_button_visible()

    def test_add_product_from_detail_page_to_cart(self):
        """TC-FP-003: Add a product from the detail page to the cart"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        self.inventory_page.click_product_by_name(product_names[0])
        
        # Verify cart is initially empty
        initial_cart_count = self.product_detail_page.get_cart_badge_count()
        
        # Add product to cart
        self.product_detail_page.add_to_cart()
        
        # Verify cart badge incremented
        updated_cart_count = self.product_detail_page.get_cart_badge_count()
        assert updated_cart_count == initial_cart_count + 1
        
        # Verify Remove button appears
        assert self.product_detail_page.is_remove_button_visible()

    def test_verify_cart_displays_correct_product_info(self):
        """TC-FP-004: Verify cart displays correct product name and price after adding from detail page"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        target_product = product_names[0]
        self.inventory_page.click_product_by_name(target_product)
        
        # Capture product details
        expected_name = self.product_detail_page.get_product_name()
        expected_price = self.product_detail_page.get_product_price()
        
        # Add to cart
        self.product_detail_page.add_to_cart()
        
        # Navigate to cart
        self.product_detail_page.go_to_cart()
        
        # Verify product in cart
        cart_item_names = self.cart_page.get_all_cart_item_names()
        assert expected_name in cart_item_names
        
        # Verify price matches
        cart_item_price = self.cart_page.get_item_price_by_name(expected_name)
        assert cart_item_price == expected_price

    def test_browser_back_button_returns_to_inventory(self):
        """TC-FP-005: Use browser back button to return to inventory page"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        self.inventory_page.click_product_by_name(product_names[0])
        
        # Verify we're on detail page
        assert "inventory-item.html" in self.product_detail_page.get_current_url()
        
        # Use browser back button
        self.page.go_back()
        
        # Verify we're back on inventory page
        assert "inventory.html" in self.page.url
        
        # Verify inventory page is displayed correctly
        inventory_products = self.inventory_page.get_all_product_names()
        assert len(inventory_products) > 0

    def test_preserve_cart_state_after_back_navigation(self):
        """TC-FP-006: Preserve cart state after returning to inventory using back button"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        self.inventory_page.click_product_by_name(product_names[0])
        
        # Add product to cart
        product_name = self.product_detail_page.get_product_name()
        self.product_detail_page.add_to_cart()
        
        # Verify cart count
        cart_count_on_detail = self.product_detail_page.get_cart_badge_count()
        assert cart_count_on_detail == 1
        
        # Use browser back button
        self.page.go_back()
        
        # Verify cart badge still shows the same count on inventory page
        cart_count_on_inventory = self.inventory_page.get_cart_badge_count()
        assert cart_count_on_inventory == cart_count_on_detail
        
        # Navigate to cart and verify product is still there
        self.inventory_page.go_to_cart()
        cart_items = self.cart_page.get_all_cart_item_names()
        assert product_name in cart_items

    def test_open_detail_for_first_and_last_inventory_items(self):
        """TC-FP-007: Open detail page for the first and last visible inventory items"""
        product_names = self.inventory_page.get_all_product_names()
        assert len(product_names) >= 2, "Need at least 2 products for this test"
        
        first_product = product_names[0]
        last_product = product_names[-1]
        
        # Open first product detail
        self.inventory_page.click_product_by_name(first_product)
        assert "inventory-item.html" in self.product_detail_page.get_current_url()
        assert self.product_detail_page.get_product_name() == first_product
        
        # Go back to inventory
        self.page.go_back()
        
        # Open last product detail
        self.inventory_page.click_product_by_name(last_product)
        assert "inventory-item.html" in self.product_detail_page.get_current_url()
        assert self.product_detail_page.get_product_name() == last_product

    def test_add_same_product_from_detail_multiple_times(self):
        """TC-FP-008: Add the same product from detail page more than once"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        target_product = product_names[0]
        self.inventory_page.click_product_by_name(target_product)
        
        product_name = self.product_detail_page.get_product_name()
        
        # Add to cart first time
        self.product_detail_page.add_to_cart()
        assert self.product_detail_page.get_cart_badge_count() == 1
        
        # Remove from cart (to enable adding again)
        self.product_detail_page.remove_from_cart()
        
        # Add to cart second time
        self.product_detail_page.add_to_cart()
        
        # Navigate back and to detail page again
        self.page.go_back()
        self.inventory_page.click_product_by_name(target_product)
        
        # Verify button shows Remove (item still in cart)
        assert self.product_detail_page.is_remove_button_visible()
        
        # Verify cart still has the item
        self.product_detail_page.go_to_cart()
        cart_items = self.cart_page.get_all_cart_item_names()
        assert product_name in cart_items

    def test_prevent_incorrect_product_data_after_navigation(self):
        """TC-FP-009: Prevent cart from showing incorrect product data after navigation"""
        product_names = self.inventory_page.get_all_product_names()
        assert len(product_names) >= 2, "Need at least 2 products for this test"
        
        first_product = product_names[0]
        second_product = product_names[1]
        
        # Open first product and add to cart
        self.inventory_page.click_product_by_name(first_product)
        first_product_name = self.product_detail_page.get_product_name()
        first_product_price = self.product_detail_page.get_product_price()
        self.product_detail_page.add_to_cart()
        
        # Navigate back
        self.page.go_back()
        
        # Open second product and add to cart
        self.inventory_page.click_product_by_name(second_product)
        second_product_name = self.product_detail_page.get_product_name()
        second_product_price = self.product_detail_page.get_product_price()
        self.product_detail_page.add_to_cart()
        
        # Go to cart
        self.product_detail_page.go_to_cart()
        
        # Verify both products are in cart with correct data
        cart_items = self.cart_page.get_all_cart_item_names()
        assert first_product_name in cart_items
        assert second_product_name in cart_items
        
        # Verify prices are correct
        assert self.cart_page.get_item_price_by_name(first_product_name) == first_product_price
        assert self.cart_page.get_item_price_by_name(second_product_name) == second_product_price

    def test_back_navigation_preserves_cart_after_page_refresh(self):
        """TC-FP-010: Back navigation does not clear cart when the inventory page is refreshed"""
        # Navigate to a product detail page
        product_names = self.inventory_page.get_all_product_names()
        target_product = product_names[0]
        self.inventory_page.click_product_by_name(target_product)
        
        # Add product to cart
        product_name = self.product_detail_page.get_product_name()
        self.product_detail_page.add_to_cart()
        cart_count = self.product_detail_page.get_cart_badge_count()
        
        # Navigate back to inventory
        self.page.go_back()
        
        # Refresh the inventory page
        self.page.reload()
        
        # Verify cart badge still shows correct count
        cart_count_after_refresh = self.inventory_page.get_cart_badge_count()
        assert cart_count_after_refresh == cart_count
        
        # Verify product is still in cart
        self.inventory_page.go_to_cart()
        cart_items = self.cart_page.get_all_cart_item_names()
        assert product_name in cart_items
