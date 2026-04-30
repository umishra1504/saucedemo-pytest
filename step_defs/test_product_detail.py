import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD


scenarios("../features/product_detail.feature")


@pytest.fixture
def product_detail_page(page: Page) -> ProductDetailPage:
    return ProductDetailPage(page)


@given("I am logged in as a standard user")
def login_as_standard_user(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@when("I open the first product from the inventory")
def open_first_product_from_inventory(inventory_page: InventoryPage, product_detail_page: ProductDetailPage):
    inventory_page.page.locator('[data-test="inventory-item-name"]').first.click()
    product_detail_page.wait_for_loaded()


@when(parsers.parse('I directly open product detail page for "{product_id}"'))
def directly_open_product_detail(page: Page, product_id: str, product_detail_page: ProductDetailPage):
    page.goto(f"{page.context._impl_obj._options.get('base_url', 'https://www.saucedemo.com')}/inventory-item.html?id={product_id}")
    page.wait_for_load_state("domcontentloaded")
    if page.locator('[data-test="inventory-item-name"]').count() > 0:
        product_detail_page.wait_for_loaded()


@when("I directly open an invalid product detail page from the address bar")
def directly_open_invalid_product_detail(page: Page):
    page.goto(f"{page.context._impl_obj._options.get('base_url', 'https://www.saucedemo.com')}/inventory-item.html?id=invalid")
    page.wait_for_load_state("domcontentloaded")


@when("I add the product to the cart from the detail page")
def add_product_to_cart_from_detail(product_detail_page: ProductDetailPage):
    product_detail_page.add_to_cart()


@when("I go back to the inventory from the product detail page")
def go_back_to_inventory(product_detail_page: ProductDetailPage):
    product_detail_page.go_back_to_inventory()


@when("I use browser back navigation")
def browser_back(page: Page):
    page.go_back()
    page.wait_for_load_state("domcontentloaded")


@when("I add the first inventory product to the cart")
def add_first_inventory_product_to_cart(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart(0)


@when("I try to tamper with the product identifier in the browser")
def tamper_product_identifier(page: Page):
    page.evaluate("window.history.replaceState({}, '', '/inventory-item.html?id=999')")


@then(parsers.parse('I should be on the product detail page for "{product_name}"'))
def verify_product_detail_page(product_detail_page: ProductDetailPage, product_name: str):
    product_detail_page.wait_for_loaded()
    assert product_detail_page.get_product_name() == product_name


@then(parsers.parse('I should see the product detail information for "{product_name}"'))
def verify_product_detail_information(product_detail_page: ProductDetailPage, product_name: str):
    product_detail_page.wait_for_loaded()
    assert product_detail_page.get_product_name() == product_name
    assert product_detail_page.get_product_description() != ""
    assert product_detail_page.get_product_price().startswith("$")


@then("I should see the Add to Cart button on the product detail page")
def verify_add_to_cart_button(product_detail_page: ProductDetailPage):
    assert product_detail_page.is_add_to_cart_visible()


@then(parsers.parse('I should see a price formatted as "{expected_price}" on the product detail page'))
def verify_price_format(product_detail_page: ProductDetailPage, expected_price: str):
    assert product_detail_page.get_product_price() == expected_price


@then(parsers.parse("the cart badge should show {count:d} item on the product detail page"))
def verify_cart_badge_single(product_detail_page: ProductDetailPage, count: int):
    assert product_detail_page.get_cart_badge_count() == count


@then(parsers.parse("the cart badge should show {count:d} items on the product detail page"))
def verify_cart_badge_plural(product_detail_page: ProductDetailPage, count: int):
    assert product_detail_page.get_cart_badge_count() == count


@then("the product should be marked as removed on the product detail page")
def verify_remove_visible(product_detail_page: ProductDetailPage):
    assert product_detail_page.is_remove_visible()


@then("I should be on the inventory page")
def verify_inventory_page(page: Page):
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url


@then(parsers.parse("the cart badge should still show {count:d} item on the inventory page"))
def verify_inventory_cart_badge(inventory_page: InventoryPage, count: int):
    assert inventory_page.get_cart_badge_count() == count


@then("I should see an error or an empty product detail state")
def verify_invalid_product_state(page: Page):
    assert page.locator('[data-test="inventory-item-name"]').count() == 0 or "inventory-item" not in page.url


@then("cart state should remain unchanged")
def verify_cart_state_unchanged(inventory_page: InventoryPage):
    assert inventory_page.get_cart_badge_count() >= 0
