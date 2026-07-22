import re

import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.orders_page import OrdersPage


@pytest.mark.smoke
def test_end_to_end_checkout_creates_an_order(registered_page: Page):
    page = registered_page
    products_page = ProductsPage(page)
    products_page.goto()
    products_page.add_to_cart_by_name("Wireless Mouse")

    cart_page = CartPage(page)
    cart_page.goto()
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(page)
    expect(checkout_page.total).to_be_visible()
    expected_total = round(checkout_page.subtotal_value() + checkout_page.shipping_value(), 2)
    assert checkout_page.total_value() == expected_total

    checkout_page.place_order()

    # order placed -> redirected to its own detail page
    expect(page).to_have_url(re.compile(r".*/orders/\d+"))

    orders_page = OrdersPage(page)
    orders_page.goto()
    latest_order = orders_page.most_recent_order_row()
    expect(latest_order).to_contain_text("placed")
    expect(latest_order).to_contain_text(f"${expected_total:.2f}")
