import re
from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductsPage(BasePage):
    path = "/products"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.get_by_test_id("live-search-input")
        self.category_select = page.get_by_test_id("category-select")
        self.sort_select = page.get_by_test_id("sort-select")
        self.product_cards = page.get_by_test_id("product-card")
        self.empty_state = page.get_by_test_id("empty-state")

    def search(self, term: str):
        # filters client-side on 'input', no submit needed
        self.search_input.fill(term)

    def filter_by_category(self, category: str):
        # select triggers a real form submit (onchange), need to wait for it
        with self.page.expect_navigation():
            self.category_select.select_option(label=category)

    def sort_by(self, label: str):
        with self.page.expect_navigation():
            self.sort_select.select_option(label=label)

    def visible_card_names(self) -> list[str]:
        names = []
        for card in self.product_cards.all():
            if card.is_visible():
                names.append(card.get_attribute("data-product-name"))
        return names

    def visible_card_prices(self) -> list[float]:
        prices = []
        for card in self.product_cards.all():
            if card.is_visible():
                text = card.get_by_test_id("product-price").inner_text()
                prices.append(float(re.sub(r"[^\d.]", "", text)))
        return prices

    def add_to_cart_by_name(self, name: str):
        card = self.product_cards.filter(has=self.page.get_by_role("heading", name=name))
        with self.page.expect_response(lambda r: "/cart/add" in r.url):
            card.get_by_test_id("add-to-cart-btn").click()

    def open_product(self, name: str):
        self.page.get_by_role("link", name=name).click()
