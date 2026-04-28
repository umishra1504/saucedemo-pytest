import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD

scenarios("../features/cart.feature")


@given("I am logged in as a standard user")
def login_as_standard_user(page: Page, login_page: LoginPage):
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@when(parsers.parse("I add product {index:d} to the cart"))
def add_product_to_cart(inventory_page: InventoryPage, index: int):
    inventory_page.add_item_to_cart(index)


@when("I go to the cart page")
def navigate_to_cart(inventory_page: InventoryPage):
    inventory_page.go_to_cart()


@when(parsers.parse("I remove item {index:d} from the cart"))
def remove_cart_item(cart_page: CartPage, index: int):
    cart_page.remove_item(index)


@when("I click continue shopping")
def click_continue_shopping(cart_page: CartPage):
    cart_page.continue_shopping()


@then(parsers.parse("I should see {count:d} item in the cart"))
def verify_cart_count(cart_page: CartPage, count: int):
    assert cart_page.get_cart_item_count() == count


@then(parsers.parse("I should see {count:d} items in the cart"))
def verify_cart_items_count(cart_page: CartPage, count: int):
    assert cart_page.get_cart_item_count() == count


@then("I should be redirected to the inventory page")
def verify_inventory_redirect(page: Page):
    page.wait_for_url("**/inventory.html")
    assert "inventory" in page.url
