"""
Test automation for Product Detail Page feature — SCRUM-172

This module contains automated tests for:
- Opening product detail pages from inventory
- Verifying product information display
- Adding products to cart from detail page
- Validating cart state and contents
- Navigation between inventory and detail pages
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
# GIVEN STEPS
# ============================================================================

@given("I am logged in as a standard user")
def login_as_standard_user(page: Page, login_page: LoginPage):
    """Log in to the application as a standard user."""
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@given("I am on the inventory page")
def verify_on_inventory_page(page: Page):
    """Verify user is on the inventory page."""
    page.wait_for_url("**/inventory.html")
    assert "inventory" in page.url


@given(parsers.parse('I click on product "{product_name}"'))
def given_click_product(page: Page, inventory_page: InventoryPage, product_name: str):
    """Navigate to product detail page (given context)."""
    product_link = page.locator(f'[data-test="item-{product_name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("t-shirt", "t-shirt")}"]')
    product_link.click()
    page.wait_for_url("**/inventory-item.html**")


@given("I add the product to cart from the detail page")
def given_add_to_cart_from_detail(product_detail_page: ProductDetailPage):
    """Add product to cart from detail page (given context)."""
    product_detail_page.add_to_cart()


@given(parsers.parse("I add product {index:d} to the cart from inventory"))
def given_add_product_from_inventory(inventory_page: InventoryPage, index: int):
    """Add product to cart from inventory page (given context)."""
    inventory_page.add_item_to_cart(index)


# ============================================================================
# WHEN STEPS
# ============================================================================

@when(parsers.parse('I click on product "{product_name}"'))
def click_on_product(page: Page, inventory_page: InventoryPage, product_name: str):
    """Click on a product to open its detail page."""
    # Map product names to their data-test attribute values
    product_map = {
        "Sauce Labs Backpack": "item-4-title-link",
        "Sauce Labs Bike Light": "item-0-title-link",
        "Sauce Labs Bolt T-Shirt": "item-1-title-link",
        "Sauce Labs Fleece Jacket": "item-5-title-link",
        "Sauce Labs Onesie": "item-2-title-link",
        "Test.allTheThings() T-Shirt (Red)": "item-3-title-link",
    }
    
    test_id = product_map.get(product_name)
    if test_id:
        page.locator(f'[data-test="{test_id}"]').click()
    else:
        # Fallback: click by visible text
        page.locator(f'text="{product_name}"').first.click()
    
    page.wait_for_url("**/inventory-item.html**")


@when("I add the product to cart from the detail page")
def add_to_cart_from_detail_page(product_detail_page: ProductDetailPage):
    """Add the currently viewed product to cart."""
    product_detail_page.add_to_cart()


@when("I click the back button")
def click_back_button(product_detail_page: ProductDetailPage):
    """Click the back button to return to inventory."""
    product_detail_page.go_back_to_inventory()


@when("I navigate to the cart page")
def navigate_to_cart(product_detail_page: ProductDetailPage):
    """Navigate to the cart page."""
    product_detail_page.go_to_cart()


@when(parsers.parse("I add product {index:d} to the cart from inventory"))
def add_product_from_inventory(inventory_page: InventoryPage, index: int):
    """Add a product to cart from the inventory page."""
    inventory_page.add_item_to_cart(index)


# ============================================================================
# THEN STEPS
# ============================================================================

@then("I should be on the product detail page")
def verify_on_product_detail_page(page: Page):
    """Verify user is on a product detail page."""
    assert "inventory-item.html" in page.url


@then(parsers.parse('the URL should contain "{url_fragment}"'))
def verify_url_contains(page: Page, url_fragment: str):
    """Verify the URL contains a specific fragment."""
    assert url_fragment in page.url


@then(parsers.parse('I should see the product name "{product_name}"'))
def verify_product_name(product_detail_page: ProductDetailPage, product_name: str):
    """Verify the product name is displayed correctly."""
    assert product_detail_page.get_product_name() == product_name


@then("I should see a product description")
def verify_product_description(product_detail_page: ProductDetailPage):
    """Verify a product description is displayed."""
    description = product_detail_page.get_product_description()
    assert description is not None
    assert len(description) > 0


@then("I should see a product price")
def verify_product_price(product_detail_page: ProductDetailPage):
    """Verify a product price is displayed."""
    price = product_detail_page.get_product_price()
    assert price is not None
    assert "$" in price


@then(parsers.parse('I should see an "{button_text}" button'))
def verify_button_visible(product_detail_page: ProductDetailPage, button_text: str):
    """Verify a specific button is visible."""
    if button_text.lower() == "add to cart":
        assert product_detail_page.is_add_to_cart_visible()


@then(parsers.parse("the cart badge should show {count:d} item"))
def verify_cart_badge_single(product_detail_page: ProductDetailPage, count: int):
    """Verify the cart badge shows the correct count (singular)."""
    assert product_detail_page.get_cart_badge_count() == count


@then(parsers.parse("the cart badge should show {count:d} items"))
def verify_cart_badge_plural(product_detail_page: ProductDetailPage, count: int):
    """Verify the cart badge shows the correct count (plural)."""
    assert product_detail_page.get_cart_badge_count() == count


@then(parsers.parse('the "{button_text}" button should be visible'))
def verify_named_button_visible(product_detail_page: ProductDetailPage, button_text: str):
    """Verify a named button is visible."""
    if button_text.lower() == "remove":
        assert product_detail_page.is_remove_button_visible()


@then(parsers.parse("I should see {count:d} item in the cart"))
def verify_cart_item_count_singular(cart_page: CartPage, count: int):
    """Verify the cart contains the correct number of items (singular)."""
    assert cart_page.get_cart_item_count() == count


@then(parsers.parse('the cart should contain product "{product_name}"'))
def verify_cart_contains_product(cart_page: CartPage, product_name: str):
    """Verify the cart contains a specific product."""
    item_names = cart_page.get_item_names()
    assert product_name in item_names


@then(parsers.parse('the cart item should have price "{price}"'))
def verify_cart_item_price(page: Page, price: str):
    """Verify a cart item has the correct price."""
    price_element = page.locator('[data-test="inventory-item-price"]').first
    assert price_element.text_content() == price


@then("I should be redirected to the inventory page")
def verify_redirected_to_inventory(page: Page):
    """Verify user is redirected to the inventory page."""
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url


@then(parsers.parse("I should see {count:d} products listed"))
def verify_products_listed(inventory_page: InventoryPage, count: int):
    """Verify the correct number of products are listed."""
    assert inventory_page.get_inventory_count() == count
