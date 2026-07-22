import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.header_component import HeaderComponent


@pytest.mark.smoke
def test_add_to_cart_updates_badge_and_cart_page(registered_page: Page):
    page = registered_page
    products_page = ProductsPage(page)
    products_page.goto()

    products_page.add_to_cart_by_name("USB-C Hub")

    header = HeaderComponent(page)
    expect(header.cart_count).to_have_text("1")

    cart_page = CartPage(page)
    cart_page.goto()
    expect(cart_page.row_for("USB-C Hub")).to_be_visible()


def test_updating_quantity_recalculates_line_and_running_totals(registered_page: Page):
    page = registered_page
    products_page = ProductsPage(page)
    products_page.goto()
    products_page.add_to_cart_by_name("Plant - Office Succulent")

    cart_page = CartPage(page)
    cart_page.goto()
    unit_price = cart_page.line_total_for("Plant - Office Succulent")

    cart_page.set_quantity("Plant - Office Succulent", 3)

    expected_line_total = round(unit_price * 3, 2)
    assert cart_page.line_total_for("Plant - Office Succulent") == expected_line_total
    assert cart_page.live_total_value() == expected_line_total
