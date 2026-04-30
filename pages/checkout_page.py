from playwright.sync_api import Page
from utils.logger import get_logger


class CheckoutPage:
    """Page Object Model for Checkout and Order Confirmation pages"""
    
    CHECKOUT_STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    CHECKOUT_STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    CHECKOUT_COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("CheckoutPage")

        # Checkout Step One - Shipping Information
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_btn = page.locator('[data-test="continue"]')
        self.cancel_btn = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')
        
        # Checkout Step Two - Order Summary
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total = page.locator('[data-test="total-label"]')
        self.finish_btn = page.locator('[data-test="finish"]')
        self.cancel_btn_step_two = page.locator('[data-test="cancel"]')
        
        # Checkout Complete - Confirmation
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')
        self.back_home_btn = page.locator('[data-test="back-to-products"]')

    # === Checkout Step One Methods ===
    
    def is_on_checkout_step_one(self) -> bool:
        """Verify user is on checkout information page"""
        return self.CHECKOUT_STEP_ONE_URL in self.page.url

    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill all shipping information fields"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.log.info(f"Filled shipping info: {first_name} {last_name}, {postal_code}")

    def enter_first_name(self, first_name: str):
        """Enter first name"""
        self.first_name_input.fill(first_name)

    def enter_last_name(self, last_name: str):
        """Enter last name"""
        self.last_name_input.fill(last_name)

    def enter_postal_code(self, postal_code: str):
        """Enter postal/zip code"""
        self.postal_code_input.fill(postal_code)

    def click_continue(self):
        """Click continue to proceed to order summary"""
        self.continue_btn.click()
        self.log.info("Clicked continue button")

    def click_cancel(self):
        """Cancel checkout and return to cart"""
        self.cancel_btn.click()
        self.log.info("Clicked cancel button")

    def get_error_message(self) -> str:
        """Get validation error message text"""
        if self.error_message.is_visible():
            return self.error_message.text_content()
        return ""

    def is_error_visible(self) -> bool:
        """Check if validation error is displayed"""
        return self.error_message.is_visible()

    def are_checkout_fields_visible(self) -> bool:
        """Verify all three required checkout fields are visible"""
        return (self.first_name_input.is_visible() and 
                self.last_name_input.is_visible() and 
                self.postal_code_input.is_visible())

    def get_field_values(self) -> dict:
        """Get current values of all shipping fields"""
        return {
            "firstName": self.first_name_input.input_value(),
            "lastName": self.last_name_input.input_value(),
            "postalCode": self.postal_code_input.input_value()
        }

    # === Checkout Step Two Methods ===

    def is_on_checkout_step_two(self) -> bool:
        """Verify user is on order summary page"""
        return self.CHECKOUT_STEP_TWO_URL in self.page.url

    def get_item_total(self) -> float:
        """Extract item subtotal from summary"""
        text = self.subtotal.text_content()
        # Format: "Item total: $XX.XX"
        return float(text.split("$")[1])

    def get_tax_amount(self) -> float:
        """Extract tax amount from summary"""
        text = self.tax.text_content()
        # Format: "Tax: $X.XX"
        return float(text.split("$")[1])

    def get_total_amount(self) -> float:
        """Extract final total from summary"""
        text = self.total.text_content()
        # Format: "Total: $XX.XX"
        return float(text.split("$")[1])

    def is_order_summary_visible(self) -> bool:
        """Check if order summary section is displayed"""
        return (self.subtotal.is_visible() and 
                self.tax.is_visible() and 
                self.total.is_visible())

    def get_cart_item_count(self) -> int:
        """Get number of items in order summary"""
        return self.cart_items.count()

    def click_finish(self):
        """Complete the order"""
        self.finish_btn.click()
        self.log.info("Clicked finish button to complete order")

    def click_cancel_on_summary(self):
        """Cancel from order summary page"""
        self.cancel_btn_step_two.click()
        self.log.info("Cancelled from order summary")

    # === Checkout Complete Methods ===

    def is_on_checkout_complete(self) -> bool:
        """Verify user is on order confirmation page"""
        return self.CHECKOUT_COMPLETE_URL in self.page.url

    def get_confirmation_header(self) -> str:
        """Get order confirmation header text"""
        return self.complete_header.text_content()

    def get_confirmation_message(self) -> str:
        """Get order confirmation message text"""
        return self.complete_text.text_content()

    def is_order_confirmed(self) -> bool:
        """Check if order confirmation is displayed"""
        return (self.is_on_checkout_complete() and 
                self.complete_header.is_visible() and
                "Thank you for your order" in self.get_confirmation_header())

    def click_back_home(self):
        """Return to products page after order completion"""
        self.back_home_btn.click()
        self.log.info("Clicked back to products")
