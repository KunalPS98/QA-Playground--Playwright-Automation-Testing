import re

import pytest
from playwright.sync_api import Page, expect

from pages.register_page import RegisterPage
from pages.header_component import HeaderComponent


@pytest.mark.smoke
def test_successful_registration_logs_the_user_in(page: Page, new_user: dict):
    register_page = RegisterPage(page)
    register_page.goto()

    register_page.register(
        new_user["name"], new_user["email"], new_user["password"], new_user["password"]
    )

    expect(page).to_have_url(re.compile(r".*/products"))
    header = HeaderComponent(page)
    expect(header.profile_link).to_have_text(new_user["name"])


# BUGS.md UI-3: confirm-password check compares the field to itself, so it
# never catches a mismatch. This should fail once someone fixes it.
@pytest.mark.bug
@pytest.mark.xfail(reason="UI-3: confirm-password check is broken", strict=True)
def test_registration_blocks_mismatched_passwords(page: Page, new_user: dict):
    register_page = RegisterPage(page)
    register_page.goto()

    register_page.register(
        new_user["name"], new_user["email"], new_user["password"], "SomeOtherPassword1"
    )

    expect(register_page.confirm_error).to_have_text("Passwords do not match.")
    expect(page).to_have_url(re.compile(r".*/register"))
