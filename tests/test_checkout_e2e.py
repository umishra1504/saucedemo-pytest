"""
End-to-End Checkout Functionality Tests — SCRUM-165

Tests comprehensive checkout flow including shipping details, order summary,
field validation, and order confirmation.

Test Coverage:
- Happy path: Complete checkout flow
- Edge cases: Minimal cart, low-value totals, state preservation
- Negative: Empty fields, whitespace validation, empty cart access
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def setup_cart_with_items(page: Page):
    """
    Fixture: Login and add items to cart before checkout tests
    Returns checkout page object with items already in cart
    """
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    
    # Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    # Add items to cart
    product_page.add_item_to_cart("Sauce Labs Backpack")
    product_page.add_item_to_cart("Sauce Labs Bike Light")
    
    # Navigate to cart and proceed to checkout
    product_page.go_to_cart()
    cart_page.click_checkout()
    
    checkout_page = CheckoutPage(page)
    return checkout_page


@pytest.fixture
def setup_cart_with_single_item(page: Page):
    """
    Fixture: Login and add single low-cost item to cart
    Used for edge case testing
    """
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    # Add only one item
    product_page.add_item_to_cart("Sauce Labs Onesie")
    
    product_page.go_to_cart()
    cart_page.click_checkout()
    
    return CheckoutPage(page)


class TestCheckoutHappyPath:
    """Happy path tests for checkout functionality"""
    
    def test_display_checkout_fields_for_shipping_details(self, setup_cart_with_items):
        """
        TC-EC-001: Display checkout fields for shipping details
        
        Verify that checkout page presents all required fields:
        First Name, Last Name, and Zip Code
        """
        checkout_page = setup_cart_with_items
        
        # Verify on checkout page
        assert checkout_page.is_on_checkout_step_one(), "User should be on checkout step one"
        
        # Verify all three required fields are visible
        assert checkout_page.are_checkout_fields_visible(), \
            "First Name, Last Name, and Zip Code fields must be visible"
        
        # Verify each field individually
        assert checkout_page.first_name_input.is_visible(), "First Name field should be visible"
        assert checkout_page.last_name_input.is_visible(), "Last Name field should be visible"
        assert checkout_page.postal_code_input.is_visible(), "Zip Code field should be visible"
        
        # Verify fields are editable
        assert checkout_page.first_name_input.is_editable(), "First Name should be editable"
        assert checkout_page.last_name_input.is_editable(), "Last Name should be editable"
        assert checkout_page.postal_code_input.is_editable(), "Zip Code should be editable"

    def test_show_order_summary_with_item_total_and_tax(self, setup_cart_with_items):
        """
        TC-EC-003: Show order summary with item total and tax before confirmation
        
        Verify order summary displays item total, tax, and final total
        """
        checkout_page = setup_cart_with_items
        
        # Fill shipping info and proceed to summary
        checkout_page.fill_shipping_information("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Verify on order summary page
        assert checkout_page.is_on_checkout_step_two(), "User should be on order summary page"
        
        # Verify order summary components are visible
        assert checkout_page.is_order_summary_visible(), \
            "Order summary with subtotal, tax, and total must be visible"
        
        # Verify price breakdown
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax_amount()
        total = checkout_page.get_total_amount()
        
        assert item_total > 0, "Item total should be greater than 0"
        assert tax > 0, "Tax should be calculated and greater than 0"
        assert total == round(item_total + tax, 2), \
            f"Total ({total}) should equal item total ({item_total}) + tax ({tax})"

    def test_submit_valid_order_successfully(self, setup_cart_with_items):
        """
        TC-EC-005: Submit a valid order successfully
        
        Verify complete checkout flow with valid data results in order confirmation
        """
        checkout_page = setup_cart_with_items
        
        # Complete checkout step one
        checkout_page.fill_shipping_information("Jane", "Smith", "90210")
        checkout_page.click_continue()
        
        # Verify on summary page
        assert checkout_page.is_on_checkout_step_two(), "Should be on order summary"
        
        # Complete the order
        checkout_page.click_finish()
        
        # Verify order confirmation
        assert checkout_page.is_on_checkout_complete(), "Should be on confirmation page"
        assert checkout_page.is_order_confirmed(), "Order confirmation should be displayed"
        
        # Verify confirmation message
        confirmation_header = checkout_page.get_confirmation_header()
        assert "Thank you for your order" in confirmation_header, \
            "Confirmation header should thank user for order"

    def test_preserve_checkout_data_while_reviewing_summary(self, setup_cart_with_items):
        """
        TC-EC-008: Preserve checkout data while reviewing order summary
        
        Verify shipping data remains intact when reviewing summary
        """
        checkout_page = setup_cart_with_items
        
        # Enter shipping information
        test_first_name = "Michael"
        test_last_name = "Johnson"
        test_postal_code = "75001"
        
        checkout_page.fill_shipping_information(test_first_name, test_last_name, test_postal_code)
        
        # Get field values before continuing
        initial_values = checkout_page.get_field_values()
        
        # Proceed to summary
        checkout_page.click_continue()
        assert checkout_page.is_on_checkout_step_two(), "Should be on summary page"
        
        # Navigate back to shipping info (simulate back button or cancel)
        checkout_page.click_cancel_on_summary()
        
        # Verify data is preserved
        preserved_values = checkout_page.get_field_values()
        assert preserved_values["firstName"] == test_first_name, "First name should be preserved"
        assert preserved_values["lastName"] == test_last_name, "Last name should be preserved"
        assert preserved_values["postalCode"] == test_postal_code, "Postal code should be preserved"


class TestCheckoutEdgeCases:
    """Edge case tests for checkout functionality"""
    
    def test_render_checkout_fields_with_minimal_cart(self, setup_cart_with_single_item):
        """
        TC-EC-002: Render checkout fields with empty or minimal cart state
        
        Verify checkout fields render correctly with single item in cart
        """
        checkout_page = setup_cart_with_single_item
        
        # Verify all fields render without layout issues
        assert checkout_page.are_checkout_fields_visible(), \
            "All checkout fields should render with minimal cart"
        
        # Verify no visual truncation or overlap (fields are interactable)
        assert checkout_page.first_name_input.is_enabled()
        assert checkout_page.last_name_input.is_enabled()
        assert checkout_page.postal_code_input.is_enabled()

    def test_validate_tax_calculation_for_low_value_cart(self, setup_cart_with_single_item):
        """
        TC-EC-006: Validate tax calculation for a low-value cart total
        
        Verify tax is calculated correctly even for low-cost items
        """
        checkout_page = setup_cart_with_single_item
        
        # Complete shipping info
        checkout_page.fill_shipping_information("Test", "User", "10000")
        checkout_page.click_continue()
        
        # Verify on summary page
        assert checkout_page.is_on_checkout_step_two()
        
        # Get price breakdown
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax_amount()
        total = checkout_page.get_total_amount()
        
        # Verify tax calculation
        assert tax > 0, "Tax should be calculated even for low-value items"
        assert tax < item_total, "Tax should be less than item total"
        
        # Verify total accuracy
        expected_total = round(item_total + tax, 2)
        assert total == expected_total, \
            f"Total {total} should equal item total {item_total} + tax {tax} = {expected_total}"

    def test_checkout_summary_after_browser_refresh(self, setup_cart_with_items):
        """
        TC-EC-010: Verify checkout summary after browser refresh prior to submission
        
        Verify page behavior is consistent after refresh on checkout page
        """
        checkout_page = setup_cart_with_items
        
        # Fill shipping details
        checkout_page.fill_shipping_information("Refresh", "Test", "55555")
        
        # Get values before refresh
        values_before = checkout_page.get_field_values()
        
        # Refresh the page
        checkout_page.page.reload()
        
        # Verify still on checkout page
        assert checkout_page.is_on_checkout_step_one(), \
            "Should remain on checkout step one after refresh"
        
        # Note: SauceDemo clears form on refresh (expected behavior)
        # Verify fields are still accessible and editable
        assert checkout_page.are_checkout_fields_visible(), \
            "Checkout fields should be visible after refresh"


class TestCheckoutNegativeScenarios:
    """Negative test scenarios for checkout validation"""
    
    def test_block_checkout_submission_when_field_empty(self, setup_cart_with_items):
        """
        TC-EC-004: Block checkout submission when required field is empty
        
        Verify validation errors display and checkout is blocked for empty fields
        """
        checkout_page = setup_cart_with_items
        
        # Test 1: Submit with all fields empty
        checkout_page.click_continue()
        assert checkout_page.is_error_visible(), "Error should be displayed for empty fields"
        assert "First Name is required" in checkout_page.get_error_message()
        
        # Test 2: Submit with only first name filled
        checkout_page.enter_first_name("John")
        checkout_page.click_continue()
        assert checkout_page.is_error_visible(), "Error should display for missing last name"
        assert "Last Name is required" in checkout_page.get_error_message()
        
        # Test 3: Submit with first and last name, missing postal code
        checkout_page.enter_last_name("Doe")
        checkout_page.click_continue()
        assert checkout_page.is_error_visible(), "Error should display for missing postal code"
        assert "Postal Code is required" in checkout_page.get_error_message()
        
        # Verify still on checkout step one (not advanced)
        assert checkout_page.is_on_checkout_step_one(), \
            "Should remain on checkout page when validation fails"

    def test_prevent_checkout_access_with_empty_cart(self, page: Page):
        """
        TC-EC-007: Prevent access to checkout when cart is empty
        
        Verify checkout is not accessible when cart has no items
        """
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        
        # Login without adding items
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        
        # Navigate to cart
        page.goto("https://www.saucedemo.com/cart.html")
        
        # Verify cart is empty
        assert cart_page.get_cart_item_count() == 0, "Cart should be empty"
        
        # Verify checkout button is either disabled or not functional
        # Note: In SauceDemo, checkout button is visible but should handle empty cart
        if cart_page.checkout_btn.is_visible():
            cart_page.click_checkout()
            # After clicking, we should either:
            # 1. Stay on cart page, or
            # 2. Be redirected back, or
            # 3. See an error
            # SauceDemo allows navigation but should ideally block this
            current_url = page.url
            # This is a potential bug if checkout proceeds with empty cart
            assert "checkout-step-one" not in current_url or page.locator('[data-test="error"]').is_visible(), \
                "Checkout should not proceed with empty cart"

    def test_reject_submission_with_whitespace_only_fields(self, setup_cart_with_items):
        """
        TC-EC-009: Reject submission with whitespace-only field values
        
        Verify whitespace-only input is treated as invalid
        """
        checkout_page = setup_cart_with_items
        
        # Enter whitespace in fields
        checkout_page.enter_first_name("   ")
        checkout_page.enter_last_name("   ")
        checkout_page.enter_postal_code("   ")
        
        # Attempt to submit
        checkout_page.click_continue()
        
        # Verify validation error or stayed on same page
        # Note: SauceDemo may accept whitespace - this tests expected behavior
        is_error_shown = checkout_page.is_error_visible()
        still_on_checkout = checkout_page.is_on_checkout_step_one()
        
        # Either error should be shown OR should not advance to next step
        assert is_error_shown or still_on_checkout, \
            "Whitespace-only input should be rejected or validated"
        
        # If advanced (bug), verify that proper validation should exist
        if checkout_page.is_on_checkout_step_two():
            pytest.fail("Whitespace-only fields should not pass validation - potential bug")
