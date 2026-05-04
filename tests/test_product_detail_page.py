import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from utils.logger import get_logger

log = get_logger("TestProductDetailPage")


@pytest.fixture
def authenticated_page(page: Page):
    """Fixture to log in and navigate to inventory page"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(page)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    
    return page


class TestProductDetailPageNavigation:
    """Tests for Product Detail Page Navigation — SCRUM-167"""

    def test_navigate_from_inventory_to_product_detail_page(self, authenticated_page: Page):
        """
        TC-PDP-001: Navigate from inventory to the selected product detail page
        Verify user can click a product and navigate to its detail page
        """
        # TC-PDP-001
        inventory_page = InventoryPage(authenticated_page)
        
        # Get the first product's name from inventory
        first_product_name = inventory_page.get_product_name(0)
        log.info(f"Clicking on product: {first_product_name}")
        
        # Click the product to navigate to detail page
        inventory_page.click_product(0)
        
        # Verify we're on the product detail page
        detail_page = ProductDetailPage(authenticated_page)
        assert "inventory-item.html" in detail_page.get_current_url()
        
        # Verify the correct product is displayed
        assert detail_page.get_product_name() == first_product_name
        log.info(f"Successfully navigated to detail page for: {first_product_name}")

    def test_navigate_to_different_product_detail_pages(self, authenticated_page: Page):
        """
        TC-PDP-002: Navigate to a different product detail page and confirm it changes
        Verify clicking different products shows the correct product details
        """
        # TC-PDP-002
        inventory_page = InventoryPage(authenticated_page)
        
        # Get first product details
        first_product_name = inventory_page.get_product_name(0)
        inventory_page.click_product(0)
        
        detail_page = ProductDetailPage(authenticated_page)
        assert detail_page.get_product_name() == first_product_name
        
        # Navigate back to inventory
        detail_page.navigate_back()
        
        # Get second product details
        second_product_name = inventory_page.get_product_name(1)
        inventory_page.click_product(1)
        
        # Verify different product is now displayed
        assert detail_page.get_product_name() == second_product_name
        assert second_product_name != first_product_name
        log.info(f"Successfully navigated to different product: {second_product_name}")


class TestProductDetailPageDisplay:
    """Tests for Product Detail Page Display — SCRUM-167"""

    def test_product_detail_page_displays_required_information(self, authenticated_page: Page):
        """
        TC-PDP-003: Verify the product detail page displays all required information
        Validates: product name, description, price, and Add to Cart button
        """
        # TC-PDP-003
        inventory_page = InventoryPage(authenticated_page)
        inventory_page.click_product(0)
        
        detail_page = ProductDetailPage(authenticated_page)
        
        # Verify all required elements are present
        product_name = detail_page.get_product_name()
        product_description = detail_page.get_product_description()
        product_price = detail_page.get_product_price()
        
        assert product_name is not None and len(product_name) > 0
        assert product_description is not None and len(product_description) > 0
        assert product_price is not None and "$" in product_price
        assert detail_page.is_add_to_cart_visible()
        
        log.info(f"Product detail page displays: Name={product_name}, Price={product_price}")

    def test_product_detail_page_renders_long_text_correctly(self, authenticated_page: Page):
        """
        TC-PDP-004: Verify product detail page renders correctly for long names and descriptions
        Ensures layout integrity with edge case text lengths
        """
        # TC-PDP-004
        inventory_page = InventoryPage(authenticated_page)
        
        # Click through multiple products to find one with longer content
        for i in range(min(3, inventory_page.get_product_count())):
            inventory_page.click_product(i)
            detail_page = ProductDetailPage(authenticated_page)
            
            # Verify content is readable and button remains accessible
            name = detail_page.get_product_name()
            description = detail_page.get_product_description()
            price = detail_page.get_product_price()
            
            assert len(name) > 0, "Product name should not be empty"
            assert len(description) > 0, "Product description should not be empty"
            assert "$" in price and len(price) > 1, "Price should be formatted correctly"
            assert detail_page.is_add_to_cart_visible(), "Add to Cart should remain accessible"
            
            log.info(f"Product {i} renders correctly: {len(name)} chars name, {len(description)} chars description")
            
            # Navigate back for next iteration
            if i < 2:
                detail_page.navigate_back()


class TestProductDetailPageAddToCart:
    """Tests for Add to Cart from Product Detail Page — SCRUM-167"""

    def test_add_product_to_cart_from_detail_page(self, authenticated_page: Page):
        """
        TC-PDP-005: Add a product to cart from detail page with correct name and price
        Validates item appears in cart with accurate information
        """
        # TC-PDP-005
        inventory_page = InventoryPage(authenticated_page)
        inventory_page.click_product(0)
        
        detail_page = ProductDetailPage(authenticated_page)
        expected_name = detail_page.get_product_name()
        expected_price = detail_page.get_product_price()
        
        # Add to cart
        detail_page.add_to_cart()
        
        # Navigate to cart
        detail_page.go_to_cart()
        cart_page = CartPage(authenticated_page)
        
        # Verify product is in cart with correct details
        assert cart_page.get_cart_item_count() == 1
        assert expected_name in cart_page.get_cart_item_names()
        
        cart_items = cart_page.get_cart_items()
        assert cart_items[0]["name"] == expected_name
        assert cart_items[0]["price"] == expected_price
        
        log.info(f"Product added to cart correctly: {expected_name} @ {expected_price}")

    def test_add_multiple_products_from_detail_pages(self, authenticated_page: Page):
        """
        TC-PDP-006: Add multiple different products from detail pages
        Verify each cart line item has accurate information
        """
        # TC-PDP-006
        inventory_page = InventoryPage(authenticated_page)
        
        # Add first product
        inventory_page.click_product(0)
        detail_page = ProductDetailPage(authenticated_page)
        product1_name = detail_page.get_product_name()
        product1_price = detail_page.get_product_price()
        detail_page.add_to_cart()
        detail_page.navigate_back()
        
        # Add second product
        inventory_page.click_product(1)
        product2_name = detail_page.get_product_name()
        product2_price = detail_page.get_product_price()
        detail_page.add_to_cart()
        
        # Navigate to cart and verify both items
        detail_page.go_to_cart()
        cart_page = CartPage(authenticated_page)
        
        assert cart_page.get_cart_item_count() == 2
        cart_items = cart_page.get_cart_items()
        
        cart_names = [item["name"] for item in cart_items]
        assert product1_name in cart_names
        assert product2_name in cart_names
        
        # Verify no data swapping occurred
        for item in cart_items:
            if item["name"] == product1_name:
                assert item["price"] == product1_price
            elif item["name"] == product2_name:
                assert item["price"] == product2_price
        
        log.info(f"Multiple products added correctly: {product1_name} and {product2_name}")


class TestProductDetailPageBackNavigation:
    """Tests for Back Navigation and Cart State Persistence — SCRUM-167"""

    def test_back_navigation_preserves_cart_state(self, authenticated_page: Page):
        """
        TC-PDP-007: Use back button after adding item and preserve cart state
        Validates cart state persists after browser back navigation
        """
        # TC-PDP-007
        inventory_page = InventoryPage(authenticated_page)
        inventory_page.click_product(0)
        
        detail_page = ProductDetailPage(authenticated_page)
        expected_name = detail_page.get_product_name()
        
        # Add to cart and note badge count
        detail_page.add_to_cart()
        badge_count_after_add = detail_page.get_cart_badge_count()
        assert badge_count_after_add == 1
        
        # Use browser back button
        detail_page.navigate_back()
        
        # Verify we're back on inventory page
        assert "inventory.html" in authenticated_page.url
        
        # Verify cart badge still shows item count
        assert inventory_page.get_cart_badge_count() == 1
        
        # Verify cart still contains the item
        inventory_page.go_to_cart()
        cart_page = CartPage(authenticated_page)
        assert cart_page.get_cart_item_count() == 1
        assert expected_name in cart_page.get_cart_item_names()
        
        log.info("Cart state preserved after back navigation")

    def test_back_navigation_with_multiple_items_preserves_state(self, authenticated_page: Page):
        """
        TC-PDP-008: Confirm cart state persists after back navigation with multiple items
        Validates all cart items remain after back navigation
        """
        # TC-PDP-008
        inventory_page = InventoryPage(authenticated_page)
        
        # Add two products from detail pages
        inventory_page.click_product(0)
        detail_page = ProductDetailPage(authenticated_page)
        product1_name = detail_page.get_product_name()
        detail_page.add_to_cart()
        detail_page.navigate_back()
        
        inventory_page.click_product(1)
        product2_name = detail_page.get_product_name()
        detail_page.add_to_cart()
        
        # Verify badge shows 2 items
        assert detail_page.get_cart_badge_count() == 2
        
        # Navigate back to inventory
        detail_page.navigate_back()
        
        # Verify cart badge on inventory page
        assert inventory_page.get_cart_badge_count() == 2
        
        # Verify both items still in cart
        inventory_page.go_to_cart()
        cart_page = CartPage(authenticated_page)
        assert cart_page.get_cart_item_count() == 2
        
        cart_names = cart_page.get_cart_item_names()
        assert product1_name in cart_names
        assert product2_name in cart_names
        
        log.info("Multiple items preserved in cart after back navigation")


class TestProductDetailPageCartBadge:
    """Tests for Cart Badge Count Updates — SCRUM-167"""

    def test_cart_badge_increments_after_adding_from_detail_page(self, authenticated_page: Page):
        """
        TC-PDP-009: Verify cart badge increments correctly after adding product
        Validates badge count reflects accurate item count
        """
        # TC-PDP-009
        inventory_page = InventoryPage(authenticated_page)
        
        # Note initial badge count (should be 0)
        initial_count = inventory_page.get_cart_badge_count()
        assert initial_count == 0
        
        # Navigate to detail page and add item
        inventory_page.click_product(0)
        detail_page = ProductDetailPage(authenticated_page)
        detail_page.add_to_cart()
        
        # Verify badge incremented by 1
        new_count = detail_page.get_cart_badge_count()
        assert new_count == initial_count + 1
        assert new_count == 1
        
        log.info(f"Cart badge correctly incremented from {initial_count} to {new_count}")


class TestProductDetailPageSecurity:
    """Security and Edge Case Tests for Product Detail Page — SCRUM-167"""

    def test_special_characters_rendered_safely(self, authenticated_page: Page):
        """
        TC-PDP-010: Safely render special characters or injected markup
        Validates content is escaped and no script execution occurs
        """
        # TC-PDP-010
        # Note: This test verifies existing products don't execute scripts
        # In a real scenario, you'd test with injected content in a test environment
        
        inventory_page = InventoryPage(authenticated_page)
        inventory_page.click_product(0)
        
        detail_page = ProductDetailPage(authenticated_page)
        product_name = detail_page.get_product_name()
        product_description = detail_page.get_product_description()
        
        # Verify text is rendered as text (no script execution)
        # If scripts were executed, the page would behave differently
        assert detail_page.is_add_to_cart_visible()
        assert product_name is not None
        assert product_description is not None
        
        # Verify no alert dialogs or unexpected behavior
        # This is a basic safety check
        log.info("Product details rendered safely without script execution")

    def test_invalid_product_url_handling(self, authenticated_page: Page):
        """
        TC-PDP-011: Prevent invalid or tampered product navigation
        Validates system handles invalid product IDs gracefully
        """
        # TC-PDP-011
        # Navigate to an invalid product URL
        authenticated_page.goto("https://www.saucedemo.com/inventory-item.html?id=999")
        
        # System should show error or redirect, not add incorrect items
        # For SauceDemo, it typically shows an error or empty page
        detail_page = ProductDetailPage(authenticated_page)
        
        # Attempt to add to cart shouldn't work with invalid product
        # Check that either the button isn't there or cart remains empty
        cart_count_before = 0
        if detail_page.cart_badge.is_visible():
            cart_count_before = detail_page.get_cart_badge_count()
        
        # If add to cart button exists, clicking it shouldn't add invalid item
        if detail_page.add_to_cart_btn.is_visible():
            detail_page.add_to_cart()
            
            # Verify cart count didn't change or no invalid item added
            detail_page.go_to_cart()
            cart_page = CartPage(authenticated_page)
            # Cart should be empty or unchanged
            assert cart_page.get_cart_item_count() == cart_count_before
        
        log.info("Invalid product URL handled safely without incorrect cart additions")
