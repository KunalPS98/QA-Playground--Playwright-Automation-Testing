import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.header_component import HeaderComponent
from pages.register_page import RegisterPage

scenarios("registration.feature")


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)


@given("I am on the registration page")
def go_to_register(register_page: RegisterPage):
    register_page.goto()


@when("I register with a new, unique account", target_fixture="new_account")
def register_new(register_page: RegisterPage, new_user: dict) -> dict:
    register_page.register(
        new_user["name"], new_user["email"], new_user["password"], new_user["password"]
    )
    return new_user


@then("I should be logged in as that new account")
def assert_registered_and_logged_in(page: Page, new_account: dict):
    header = HeaderComponent(page)
    expect(header.profile_link).to_have_text(new_account["name"])
