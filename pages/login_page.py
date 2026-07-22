from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_test_id("login-email")
        self.password_input = page.get_by_test_id("login-password")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error_banner = page.get_by_test_id("login-error")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
