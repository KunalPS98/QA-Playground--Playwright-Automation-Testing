import pytest
from playwright.sync_api import Page, expect

from pages.admin_products_page import AdminProductsPage
from pages.header_component import HeaderComponent
from utils.test_data import unique_suffix


def test_non_admin_cannot_access_admin_dashboard(registered_page: Page):
    page = registered_page
    header = HeaderComponent(page)
    expect(header.admin_link).to_be_hidden()

    page.goto("/admin")

    expect(page.get_by_role("heading")).to_have_text("403 - Forbidden")


@pytest.mark.smoke
def test_admin_can_add_and_delete_a_product(admin_page: Page):
    header = HeaderComponent(admin_page)
    expect(header.admin_link).to_be_visible()

    admin_products = AdminProductsPage(admin_page)
    admin_products.goto()

    name = f"Test Widget {unique_suffix()}"
    admin_products.open_add_modal()
    admin_products.fill_new_product(f"SKU-{unique_suffix()}", name, "Test", 9.99, 5)
    admin_products.save_product()

    expect(admin_products.row_for(name)).to_be_visible()

    admin_products.open_delete_modal(name)
    admin_products.confirm_delete()

    expect(admin_products.row_for(name)).to_have_count(0)


def test_delete_modal_closes_on_cancel(admin_page: Page):
    admin_products = AdminProductsPage(admin_page)
    admin_products.goto()

    admin_products.rows.first.get_by_test_id("delete-product-btn").click()
    expect(admin_products.delete_modal_overlay).to_be_visible()

    admin_products.cancel_delete_btn.click()
    expect(admin_products.delete_modal_overlay).to_be_hidden()


# BUGS.md UI-7: unlike the add/edit product modal, the delete modal has no
# click handler on its backdrop, so clicking outside it does nothing.
@pytest.mark.bug
@pytest.mark.xfail(reason="UI-7: delete modal doesn't close on outside click", strict=True)
def test_delete_modal_closes_on_outside_click(admin_page: Page):
    admin_products = AdminProductsPage(admin_page)
    admin_products.goto()

    admin_products.rows.first.get_by_test_id("delete-product-btn").click()
    expect(admin_products.delete_modal_overlay).to_be_visible()

    admin_products.click_delete_overlay_backdrop()
    expect(admin_products.delete_modal_overlay).to_be_hidden()
