import re
from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart"

    def __init__(self, page: Page):
        super().__init__(page)
        self.rows = page.get_by_test_id("cart-row")
        self.subtotal = page.get_by_test_id("cart-subtotal")
        self.live_total = page.get_by_test_id("cart-live-total")
        self.checkout_button = page.get_by_test_id("checkout-btn")
        self.empty_state = page.get_by_test_id("cart-empty")

    def row_for(self, product_name: str):
        return self.rows.filter(has_text=product_name)

    def set_quantity(self, product_name: str, quantity: int):
        row = self.row_for(product_name)
        qty_input = row.get_by_test_id("cart-qty-input")
        qty_input.fill(str(quantity))
        qty_input.press("Tab")

    def line_total_for(self, product_name: str) -> float:
        text = self.row_for(product_name).get_by_test_id("cart-line-total").inner_text()
        return float(re.sub(r"[^\d.]", "", text))

    def live_total_value(self) -> float:
        return float(re.sub(r"[^\d.]", "", self.live_total.inner_text()))

    def proceed_to_checkout(self):
        self.checkout_button.click()
