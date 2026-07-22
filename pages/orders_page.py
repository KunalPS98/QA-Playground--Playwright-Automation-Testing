from playwright.sync_api import Page
from pages.base_page import BasePage


class OrdersPage(BasePage):
    path = "/orders"

    def __init__(self, page: Page):
        super().__init__(page)
        self.order_rows = page.get_by_test_id("order-row")
        self.empty_state = page.get_by_test_id("orders-empty")

    def most_recent_order_row(self):
        # Orders are rendered newest-first.
        return self.order_rows.first
