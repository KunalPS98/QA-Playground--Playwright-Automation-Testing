import pytest

from utils.test_data import unique_suffix


def test_list_products_returns_all_products(anon_client):
    resp = anon_client.list_products()

    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == len(body["products"])
    assert body["count"] > 0


def test_get_single_product_returns_numeric_price(anon_client):
    resp = anon_client.get_product(1)

    assert resp.status_code == 200
    assert isinstance(resp.json()["product"]["price"], (int, float))


# BUGS.md API-5: product id 2 returns price as a string, unlike every
# other product.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-5: product 2 returns price as a string", strict=True)
def test_product_two_price_is_also_numeric(anon_client):
    resp = anon_client.get_product(2)

    assert isinstance(resp.json()["product"]["price"], (int, float))


def test_get_nonexistent_product_returns_404(anon_client):
    resp = anon_client.get_product(999999)

    assert resp.status_code == 404


# BUGS.md API-6: negative price/stock should be rejected with 400.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-6: no validation on negative price/stock", strict=True)
def test_create_product_rejects_negative_price_and_stock(created_products):
    resp = created_products(
        sku=f"NEG-{unique_suffix()}",
        name="Negative Test Product",
        category="Test",
        price=-10,
        stock=-5,
    )

    assert resp.status_code == 400


# BUGS.md API-4 / DB-1: a PUT that updates price is silently dropped in
# the database, even though the response echoes back the new price.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-4: price updates never persist", strict=True)
def test_updating_price_persists(admin_client, created_products):
    create_resp = created_products(
        sku=f"PRICE-{unique_suffix()}",
        name="Price Update Test Product",
        category="Test",
        price=10.00,
        stock=1,
    )
    product_id = create_resp.json()["product"]["id"]

    admin_client.update_product(product_id, price=25.00)

    refetched = admin_client.get_product(product_id)
    assert refetched.json()["product"]["price"] == 25.00


# BUGS.md API-3: deleting a product id that doesn't exist should 404.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-3: deleting a nonexistent product returns 200", strict=True)
def test_delete_nonexistent_product_returns_404(admin_client):
    resp = admin_client.delete_product(999999)

    assert resp.status_code == 404


def test_create_product_requires_admin(customer_client):
    resp = customer_client.create_product(
        sku=f"NOPE-{unique_suffix()}", name="Should Fail", category="Test", price=1
    )

    assert resp.status_code == 403
