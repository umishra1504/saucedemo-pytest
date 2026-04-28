import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage

scenarios("../features/login.feature")


@given("I am on the login page")
def navigate_to_login(login_page: LoginPage):
    login_page.navigate()


@when(parsers.re(r'I enter username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"'))
def enter_credentials(login_page: LoginPage, username: str, password: str):
    login_page.username_input.fill(username)
    login_page.password_input.fill(password)


@when("I click the login button")
def click_login(login_page: LoginPage):
    login_page.login_button.click()


@then("I should be redirected to the inventory page")
def verify_inventory_redirect(page: Page):
    page.wait_for_url("**/inventory.html")
    assert "inventory" in page.url


@then(parsers.parse('I should see an error message containing "{text}"'))
def verify_error_message(login_page: LoginPage, text: str):
    assert login_page.is_error_displayed()
    assert text in login_page.get_error_message()
