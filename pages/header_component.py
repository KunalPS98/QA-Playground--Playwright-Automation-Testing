from playwright.sync_api import Page


class HeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.get_by_test_id("nav-cart")
        self.cart_count = page.get_by_test_id("cart-count")
        self.login_link = page.get_by_test_id("nav-login")
        self.profile_link = page.get_by_test_id("nav-profile")
        self.admin_link = page.get_by_test_id("nav-admin")
        self.logout_button = page.get_by_test_id("logout-btn")

    def cart_count_value(self) -> int:
        return int(self.cart_count.inner_text())

    def open_cart(self):
        self.cart_link.click()
