from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page
from slugify import slugify

from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.test_data import new_user_payload, SAMPLE_ADMIN

ARTIFACTS_DIR = Path("reports/artifacts")

_ATTACHMENT_TYPES = {
    ".png": allure.attachment_type.PNG,
    ".webm": allure.attachment_type.WEBM,
    ".zip": allure.attachment_type.ZIP,
}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "teardown" or not getattr(item, "rep_call", None):
        return
    if not item.rep_call.failed:
        return

    test_dir = ARTIFACTS_DIR / slugify(item.nodeid)
    if not test_dir.exists():
        return

    for file in test_dir.iterdir():
        attachment_type = _ATTACHMENT_TYPES.get(file.suffix)
        if attachment_type:
            allure.attach.file(str(file), name=file.name, attachment_type=attachment_type)


@pytest.fixture
def new_user() -> dict:
    return new_user_payload()


@pytest.fixture
def registered_page(page: Page, new_user: dict) -> Page:
    # registration logs you in automatically, cheapest way to get an
    # authenticated session for cart/checkout/orders tests
    register_page = RegisterPage(page)
    register_page.goto()
    register_page.register(
        new_user["name"], new_user["email"], new_user["password"], new_user["password"]
    )
    page.wait_for_url("**/products")
    return page


@pytest.fixture
def admin_page(page: Page) -> Page:
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(SAMPLE_ADMIN["email"], SAMPLE_ADMIN["password"])
    page.wait_for_load_state()
    return page
