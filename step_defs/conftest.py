import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Pre-authenticated page — logs in as standard user."""
    lp = LoginPage(page)
    lp.navigate()
    lp.login(STANDARD_USER, STANDARD_PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
