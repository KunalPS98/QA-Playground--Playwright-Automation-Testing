from playwright.sync_api import Page
from pages.base_page import BasePage


class RegisterPage(BasePage):
    path = "/register"

    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = page.get_by_test_id("register-name")
        self.email_input = page.get_by_test_id("register-email")
        self.password_input = page.get_by_test_id("register-password")
        self.confirm_password_input = page.get_by_test_id("register-confirm-password")
        self.submit_button = page.get_by_test_id("register-submit")
        self.error_banner = page.get_by_test_id("register-error")
        self.confirm_error = page.get_by_test_id("register-confirm-error")

    def register(self, name: str, email: str, password: str, confirm_password: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirm_password_input.fill(confirm_password)
        self.submit_button.click()
