from playwright.sync_api import Page
from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    path = "/admin/products"

    def __init__(self, page: Page):
        super().__init__(page)
        self.open_add_modal_btn = page.get_by_test_id("open-add-product-modal")
        self.product_modal_overlay = page.get_by_test_id("product-modal-overlay")
        self.sku_input = page.get_by_test_id("pf-sku")
        self.name_input = page.get_by_test_id("pf-name")
        self.category_input = page.get_by_test_id("pf-category")
        self.price_input = page.get_by_test_id("pf-price")
        self.stock_input = page.get_by_test_id("pf-stock")
        self.save_btn = page.get_by_test_id("save-product-btn")
        self.rows = page.get_by_test_id("admin-product-row")
        self.delete_modal_overlay = page.get_by_test_id("delete-modal-overlay")
        self.confirm_delete_btn = page.get_by_test_id("confirm-delete-btn")
        self.cancel_delete_btn = page.get_by_test_id("cancel-delete-modal")

    def row_for(self, name: str):
        return self.rows.filter(has_text=name)

    def open_add_modal(self):
        self.open_add_modal_btn.click()

    def fill_new_product(self, sku: str, name: str, category: str, price: float, stock: int):
        self.sku_input.fill(sku)
        self.name_input.fill(name)
        self.category_input.fill(category)
        self.price_input.fill(str(price))
        self.stock_input.fill(str(stock))

    def save_product(self):
        with self.page.expect_response(lambda r: "/admin/products" in r.url):
            self.save_btn.click()

    def open_delete_modal(self, name: str):
        self.row_for(name).get_by_test_id("delete-product-btn").click()

    def click_delete_overlay_backdrop(self):
        # click near the corner of the overlay, away from the modal card
        self.delete_modal_overlay.click(position={"x": 10, "y": 10})

    def confirm_delete(self):
        with self.page.expect_response(lambda r: "/delete" in r.url):
            self.confirm_delete_btn.click()
