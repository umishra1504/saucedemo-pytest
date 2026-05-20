import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


class TestCheckoutFunctionality:
    """Tests for End-to-end Checkout Functionality — SCRUM-170"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup: Login and add items to cart before each test"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        
        product_page = ProductPage(page)
        product_page.add_to_cart("Sauce Labs Backpack")
        
        self.page = page
        self.product_page = product_page
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.overview_page = CheckoutOverviewPage(page)
        self.complete_page = CheckoutCompletePage(page)

    def test_proceed_to_checkout_from_cart_with_items(self):
        """TC-CHECKOUT-001: Proceed to checkout from cart with items"""
        # Navigate to cart
        self.product_page.navigate_to_cart()
        
        # Verify items in cart
        assert self.cart_page.get_cart_item_count() > 0, "Cart should have items"
        
        # Proceed to checkout
        self.cart_page.proceed_to_checkout()
        
        # Verify user is on checkout page
        assert self.checkout_page.is_on_checkout_page(), "Should navigate to checkout page"

    def test_complete_purchase_with_valid_shipping_information(self):
        """TC-CHECKOUT-002: Complete purchase with valid shipping information"""
        # Navigate to checkout
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill shipping information
        self.checkout_page.fill_shipping_info("John", "Doe", "12345")
        self.checkout_page.click_continue()
        
        # Verify on overview page with order summary
        assert self.overview_page.is_on_overview_page(), "Should be on order overview page"
        assert self.overview_page.is_item_total_displayed(), "Item total should be displayed"
        assert self.overview_page.is_tax_displayed(), "Tax should be displayed"
        
        # Complete purchase
        self.overview_page.click_finish()
        
        # Verify purchase completion
        assert self.complete_page.is_order_complete(), "Order should be completed successfully"
        assert "THANK YOU" in self.complete_page.get_confirmation_header().upper(), "Confirmation header should display thank you message"

    def test_display_item_total_and_tax_before_purchase_completion(self):
        """TC-CHECKOUT-003: Display item total and tax before purchase completion"""
        # Navigate through checkout with shipping info
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_shipping_info("Jane", "Smith", "90210")
        self.checkout_page.click_continue()
        
        # Verify order summary elements are displayed
        assert self.overview_page.is_on_overview_page(), "Should be on order overview page"
        assert self.overview_page.is_item_total_displayed(), "Item total must be displayed before purchase"
        assert self.overview_page.is_tax_displayed(), "Tax must be displayed before purchase"
        
        # Verify values are numeric and valid
        item_total = self.overview_page.get_item_total()
        tax = self.overview_page.get_tax()
        total = self.overview_page.get_total()
        
        assert item_total > 0, "Item total should be greater than 0"
        assert tax > 0, "Tax should be greater than 0"
        assert total == item_total + tax, "Total should equal item total plus tax"

    def test_block_checkout_submission_when_first_name_is_empty(self):
        """TC-CHECKOUT-007: Block checkout submission when first name is empty"""
        # Navigate to checkout
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only last name and zip code, leave first name empty
        self.checkout_page.fill_shipping_info("", "Doe", "12345")
        self.checkout_page.click_continue()
        
        # Verify validation error is displayed
        assert self.checkout_page.is_error_displayed(), "Validation error should be displayed"
        error_msg = self.checkout_page.get_error_message()
        assert "first name" in error_msg.lower(), "Error should mention first name field"
        
        # Verify still on checkout page (not progressed)
        assert self.checkout_page.is_on_checkout_page(), "Should remain on checkout page when validation fails"

    def test_block_checkout_submission_when_last_name_is_empty(self):
        """TC-CHECKOUT-008: Block checkout submission when last name is empty"""
        # Navigate to checkout
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only first name and zip code, leave last name empty
        self.checkout_page.fill_shipping_info("John", "", "12345")
        self.checkout_page.click_continue()
        
        # Verify validation error is displayed
        assert self.checkout_page.is_error_displayed(), "Validation error should be displayed"
        error_msg = self.checkout_page.get_error_message()
        assert "last name" in error_msg.lower(), "Error should mention last name field"
        
        # Verify still on checkout page
        assert self.checkout_page.is_on_checkout_page(), "Should remain on checkout page when validation fails"

    def test_reject_checkout_submission_with_empty_zip_code(self):
        """TC-CHECKOUT-009: Reject checkout submission with empty zip code"""
        # Navigate to checkout
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Fill only first and last name, leave zip code empty
        self.checkout_page.fill_shipping_info("John", "Doe", "")
        self.checkout_page.click_continue()
        
        # Verify validation error is displayed
        assert self.checkout_page.is_error_displayed(), "Validation error should be displayed"
        error_msg = self.checkout_page.get_error_message()
        assert "postal" in error_msg.lower() or "zip" in error_msg.lower(), "Error should mention zip/postal code field"
        
        # Verify still on checkout page
        assert self.checkout_page.is_on_checkout_page(), "Should remain on checkout page when validation fails"

    def test_accept_zip_code_at_valid_boundary_length(self):
        """TC-CHECKOUT-005: Accept zip code at valid boundary length"""
        # Navigate to checkout
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        
        # Test with minimum valid zip code (5 digits)
        self.checkout_page.fill_shipping_info("John", "Doe", "12345")
        self.checkout_page.click_continue()
        
        # Verify successful progression to overview page
        assert self.overview_page.is_on_overview_page(), "Should accept valid 5-digit zip code and proceed"
        
        # Go back and test with extended zip code format (9 digits)
        self.page.go_back()
        self.checkout_page.fill_shipping_info("Jane", "Smith", "123456789")
        self.checkout_page.click_continue()
        
        # Verify successful progression
        assert self.overview_page.is_on_overview_page(), "Should accept valid extended zip code and proceed"

    def test_preserve_order_summary_values_when_shipping_fields_edited(self):
        """TC-CHECKOUT-006: Preserve order summary values when shipping fields are edited"""
        # Navigate through checkout to overview page
        self.product_page.navigate_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_shipping_info("John", "Doe", "12345")
        self.checkout_page.click_continue()
        
        # Capture initial order summary values
        initial_item_total = self.overview_page.get_item_total()
        initial_tax = self.overview_page.get_tax()
        initial_total = self.overview_page.get_total()
        
        # Go back to shipping page and edit fields
        self.page.go_back()
        assert self.checkout_page.is_on_checkout_page(), "Should be back on checkout page"
        
        # Edit shipping information
        self.checkout_page.fill_shipping_info("Jane", "Smith", "90210")
        self.checkout_page.click_continue()
        
        # Verify order summary values remain unchanged
        updated_item_total = self.overview_page.get_item_total()
        updated_tax = self.overview_page.get_tax()
        updated_total = self.overview_page.get_total()
        
        assert initial_item_total == updated_item_total, "Item total should not change when shipping info is edited"
        assert initial_tax == updated_tax, "Tax should not change when shipping info is edited"
        assert initial_total == updated_total, "Total should not change when shipping info is edited"
