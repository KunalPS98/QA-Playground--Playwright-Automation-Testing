import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.header_component import HeaderComponent
from utils.test_data import SAMPLE_CUSTOMER


@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.goto()

    login_page.login(SAMPLE_CUSTOMER["email"], SAMPLE_CUSTOMER["password"])

    # no ?next= param, so /login sends you home rather than to /products
    expect(page).not_to_have_url(re.compile(r".*/login"))
    header = HeaderComponent(page)
    expect(header.profile_link).to_be_visible()
    expect(header.login_link).to_be_hidden()


def test_login_with_invalid_password_shows_error(page: Page):
    login_page = LoginPage(page)
    login_page.goto()

    login_page.login(SAMPLE_CUSTOMER["email"], "definitely-the-wrong-password")

    expect(login_page.error_banner).to_have_text("Invalid email or password.")
    expect(page).to_have_url(re.compile(r".*/login"))
