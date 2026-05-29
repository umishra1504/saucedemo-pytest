"""
Test steps for Product Detail Page feature - SCRUM-172

Automated test coverage for product detail page functionality including:
- Navigating to product detail pages from inventory
- Verifying product information display
- Adding products to cart from detail page
- Verifying cart state and navigation
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD

# Load all scenarios from the product_detail.feature file
scenarios("../features/product_detail.feature")


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def product_detail_page(page: Page) -> ProductDetailPage:
    """Fixture to provide ProductDetailPage instance."""
    return ProductDetailPage(page)


# ============================================================================
# GIVEN STEPS
# ============================================================================

@given("I am logged in as a standard user")
def login_as_standard_user(page: Page, login_page: LoginPage):
    """TC-SCRUM-172-001 to 006: Log in as standard user."""
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@given("I am on the inventory page")
def verify_on_inventory_page(page: Page):
    """TC-SCRUM-172-001 to 006: Verify user is on inventory page."""
    assert "inventory.html" in page.url


# ============================================================================
# WHEN STEPS
# ============================================================================

@when(parsers.parse('I click on product "{product_name}" from the inventory'))
def click_product_from_inventory(page: Page, product_name: str, inventory_page: InventoryPage):
    """TC-SCRUM-172-001, 002, 003, 004, 005, 006: Click product to open detail page."""
    # Find and click the product link by name
    product_link = page.locator(f'[data-test="item-{_get_product_id(product_name)}-title-link"]')
    product_link.click()
    page.wait_for_url("**/inventory-item.html**")


@when("I add the product to cart from the detail page")
def add_to_cart_from_detail(product_detail_page: ProductDetailPage):
    """TC-SCRUM-172-003, 004, 006: Add product to cart from detail page."""
    product_detail_page.add_to_cart()


@when("I go to the cart page")
def navigate_to_cart_from_detail(product_detail_page: ProductDetailPage):
    """TC-SCRUM-172-004: Navigate to cart from detail page."""
    product_detail_page.go_to_cart()


@when("I click the back to products button")
def click_back_button(product_detail_page: ProductDetailPage):
    """TC-SCRUM-172-005, 006: Click back button to return to inventory."""
    product_detail_page.click_back_to_products()


@when(parsers.parse("I add product {index:d} to the cart"))
def add_product_from_inventory(inventory_page: InventoryPage, index: int):
    """TC-SCRUM-172-006: Add product to cart from inventory page."""
    inventory_page.add_item_to_cart(index)


# ============================================================================
# THEN STEPS
# ============================================================================

@then("I should be on the product detail page")
def verify_on_detail_page(product_detail_page: ProductDetailPage):
    """TC-SCRUM-172-001: Verify on product detail page."""
    assert product_detail_page.is_on_detail_page()


@then(parsers.parse('the URL should contain "{url_fragment}"'))
def verify_url_contains(page: Page, url_fragment: str):
    """TC-SCRUM-172-001, 005: Verify URL contains expected fragment."""
    assert url_fragment in page.url


@then(parsers.parse('I should see the product name "{product_name}"'))
def verify_product_name(product_detail_page: ProductDetailPage, product_name: str):
    """TC-SCRUM-172-002: Verify product name is displayed correctly."""
    assert product_detail_page.is_product_name_visible()
    assert product_detail_page.get_product_name() == product_name


@then("I should see the product description")
def verify_product_description(product_detail_page: ProductDetailPage):
    """TC-SCRUM-172-002: Verify product description is visible."""
    assert product_detail_page.is_product_description_visible()
    description = product_detail_page.get_product_description()
    assert len(description) > 0


@then(parsers.parse('I should see the product price "{price}"'))
def verify_product_price(product_detail_page: ProductDetailPage, price: str):
    """TC-SCRUM-172-002: Verify product price is displayed correctly."""
    assert product_detail_page.is_product_price_visible()
    assert product_detail_page.get_product_price() == price


@then(parsers.parse('I should see the "{button_text}" button'))
def verify_button_visible(product_detail_page: ProductDetailPage, button_text: str):
    """TC-SCRUM-172-002: Verify Add to cart button is visible."""
    assert product_detail_page.is_add_to_cart_visible()


@then(parsers.parse("the cart badge should show {count:d} item"))
def verify_cart_badge_count_singular(product_detail_page: ProductDetailPage, count: int):
    """TC-SCRUM-172-003: Verify cart badge shows correct count."""
    assert product_detail_page.get_cart_badge_count() == count


@then(parsers.parse("the cart badge should show {count:d} items"))
def verify_cart_badge_count_plural(product_detail_page: ProductDetailPage, count: int):
    """TC-SCRUM-172-006: Verify cart badge shows correct count (plural)."""
    assert product_detail_page.get_cart_badge_count() == count


@then(parsers.parse("the cart badge should still show {count:d} items"))
def verify_cart_badge_persists(inventory_page: InventoryPage, count: int):
    """TC-SCRUM-172-006: Verify cart badge count persists after navigation."""
    assert inventory_page.get_cart_badge_count() == count


@then(parsers.parse('the "{button_text}" button should be displayed'))
def verify_remove_button_visible(product_detail_page: ProductDetailPage, button_text: str):
    """TC-SCRUM-172-003: Verify Remove button appears after adding to cart."""
    assert product_detail_page.remove_button.is_visible()


@then(parsers.parse('I should see "{product_name}" in the cart'))
def verify_product_in_cart(cart_page: CartPage, product_name: str):
    """TC-SCRUM-172-004: Verify product appears in cart with correct name."""
    cart_items = cart_page.get_item_names()
    assert product_name in cart_items


@then(parsers.parse('the cart item price should be "{price}"'))
def verify_cart_item_price(page: Page, price: str):
    """TC-SCRUM-172-004: Verify cart item shows correct price."""
    price_element = page.locator('[data-test="inventory-item-price"]').first
    assert price_element.text_content() == price


@then("I should be redirected to the inventory page")
def verify_inventory_redirect(page: Page):
    """TC-SCRUM-172-005, 006: Verify redirect to inventory page."""
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_product_id(product_name: str) -> int:
    """
    Map product names to their data-test IDs on SauceDemo.
    
    Args:
        product_name: Full product name
        
    Returns:
        Product ID for data-test attribute
    """
    product_map = {
        "Sauce Labs Backpack": 4,
        "Sauce Labs Bike Light": 0,
        "Sauce Labs Bolt T-Shirt": 1,
        "Sauce Labs Fleece Jacket": 5,
        "Sauce Labs Onesie": 2,
        "Test.allTheThings() T-Shirt (Red)": 3,
    }
    return product_map.get(product_name, 4)  # Default to backpack if not found
