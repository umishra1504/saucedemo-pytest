import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import STANDARD_PASSWORD, STANDARD_USER

scenarios("../features/checkout.feature")


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@given("I am logged in as a standard user")
def login_as_standard_user(page: Page, login_page: LoginPage):
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@given("I have an item in the cart")
def item_in_cart(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart(0)


@given("I have multiple items in the cart")
def multiple_items_in_cart(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(1)


@when("I go to the cart page")
def go_to_cart(inventory_page: InventoryPage):
    inventory_page.go_to_cart()


@when("I proceed to checkout")
def proceed_to_checkout(cart_page: CartPage):
    cart_page.proceed_to_checkout()


@when(parsers.parse('I enter shipping information with first name "{first_name}", last name "{last_name}", and zip code "{zip_code}"'))
def enter_shipping_information(checkout_page: CheckoutPage, first_name: str, last_name: str, zip_code: str):
    checkout_page.fill_shipping_information(first_name, last_name, zip_code)


@when("I continue checkout")
def continue_checkout(checkout_page: CheckoutPage):
    checkout_page.continue_checkout()


@when("I finish the purchase")
def finish_purchase(checkout_page: CheckoutPage):
    checkout_page.finish_checkout()


@then("I should see the checkout information page")
def verify_checkout_step_one(page: Page):
    page.wait_for_url("**/checkout-step-one.html")
    assert "checkout-step-one" in page.url


@then("I should see the checkout overview page")
def verify_checkout_step_two(page: Page):
    page.wait_for_url("**/checkout-step-two.html")
    assert "checkout-step-two" in page.url


@then("I should see the order complete page")
def verify_checkout_complete(page: Page, checkout_page: CheckoutPage):
    page.wait_for_url("**/checkout-complete.html")
    assert "checkout-complete" in page.url
    assert "Thank you" in checkout_page.get_complete_header()


@then("I should see a validation error")
def verify_validation_error(checkout_page: CheckoutPage):
    assert checkout_page.get_error_message() != ""


@then("I should see item total and tax in the order summary")
def verify_summary_amounts(checkout_page: CheckoutPage):
    assert checkout_page.get_subtotal().startswith("Item total: $")
    assert checkout_page.get_tax().startswith("Tax: $")
    assert checkout_page.get_total().startswith("Total: $")


@then(parsers.parse("the shipping fields should accept first name {first_name}, last name {last_name}, zip code {zip_code}"))
def verify_boundary_shipping_values(checkout_page: CheckoutPage, first_name: str, last_name: str, zip_code: str):
    assert checkout_page.first_name_input.input_value() == first_name
    assert checkout_page.last_name_input.input_value() == last_name
    assert checkout_page.zip_code_input.input_value() == zip_code
