import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD

scenarios("../features/inventory.feature")


@given("I am logged in as a standard user")
def login_as_standard_user(page: Page, login_page: LoginPage, inventory_page: InventoryPage):
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")


@then(parsers.parse('I should see the inventory page title "{title}"'))
def verify_page_title(inventory_page: InventoryPage, title: str):
    assert inventory_page.get_page_title() == title


@then(parsers.parse("I should see {count:d} products listed"))
def verify_product_count(inventory_page: InventoryPage, count: int):
    assert inventory_page.get_inventory_count() == count


@when(parsers.parse('I sort products by "{sort_option}"'))
def sort_products(inventory_page: InventoryPage, sort_option: str):
    inventory_page.sort_by(sort_option)


@then(parsers.parse('the first product should be "{product_name}"'))
def verify_first_product(inventory_page: InventoryPage, product_name: str):
    names = inventory_page.get_item_names()
    assert names[0] == product_name


@when(parsers.parse("I add product {index:d} to the cart"))
def add_product_to_cart(inventory_page: InventoryPage, index: int):
    inventory_page.add_item_to_cart(index)


@then(parsers.parse("the cart badge should show {count:d} item"))
def verify_cart_badge(inventory_page: InventoryPage, count: int):
    assert inventory_page.get_cart_badge_count() == count
