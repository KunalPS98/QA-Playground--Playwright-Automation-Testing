import re
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout"

    def __init__(self, page: Page):
        super().__init__(page)
        self.subtotal = page.get_by_test_id("checkout-subtotal")
        self.shipping = page.get_by_test_id("checkout-shipping")
        self.total = page.get_by_test_id("checkout-total")
        self.place_order_button = page.get_by_test_id("place-order-btn")

    def _money(self, locator) -> float:
        return float(re.sub(r"[^\d.]", "", locator.inner_text()))

    def subtotal_value(self) -> float:
        return self._money(self.subtotal)

    def shipping_value(self) -> float:
        return self._money(self.shipping)

    def total_value(self) -> float:
        return self._money(self.total)

    def place_order(self):
        self.place_order_button.click()
