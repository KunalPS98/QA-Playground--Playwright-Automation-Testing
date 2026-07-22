import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.header_component import HeaderComponent
from pages.login_page import LoginPage
from utils.test_data import SAMPLE_CUSTOMER

scenarios("login.feature")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@given("I am on the login page")
def go_to_login(login_page: LoginPage):
    login_page.goto()


@when("I log in with a valid sample account")
def login_valid(login_page: LoginPage):
    login_page.login(SAMPLE_CUSTOMER["email"], SAMPLE_CUSTOMER["password"])


@when("I log in with the wrong password")
def login_invalid(login_page: LoginPage):
    login_page.login(SAMPLE_CUSTOMER["email"], "definitely-the-wrong-password")


@then("I should be logged in")
def assert_logged_in(page: Page):
    header = HeaderComponent(page)
    expect(header.profile_link).to_be_visible()


@then(parsers.parse('I should see an "{message}" error'))
def assert_login_error(login_page: LoginPage, message: str):
    expect(login_page.error_banner).to_have_text(message)
