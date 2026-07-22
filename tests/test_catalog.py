import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage


# BUGS.md UI-5: quick filter does a case-sensitive substring match, so
# lowercase queries miss title-cased product names.
@pytest.mark.bug
@pytest.mark.xfail(reason="UI-5: quick filter is case-sensitive", strict=True)
def test_quick_filter_search_is_case_insensitive(page: Page):
    products_page = ProductsPage(page)
    products_page.goto()

    products_page.search("keyboard")

    assert "Mechanical Keyboard" in products_page.visible_card_names()


@pytest.mark.smoke
def test_filter_by_category_shows_only_that_category(page: Page):
    products_page = ProductsPage(page)
    products_page.goto()

    products_page.filter_by_category("Electronics")

    expect(products_page.product_cards.first).to_be_visible()
    for card in products_page.product_cards.all():
        expect(card.get_by_test_id("product-category")).to_have_text("Electronics")


# BUGS.md UI-6: "Price: Low to High" is wired to the wrong sort direction.
@pytest.mark.bug
@pytest.mark.xfail(reason="UI-6: low-to-high sort is reversed", strict=True)
def test_sort_price_low_to_high_is_ascending(page: Page):
    products_page = ProductsPage(page)
    products_page.goto()

    products_page.sort_by("Price: Low to High")

    prices = products_page.visible_card_prices()
    assert prices == sorted(prices)
