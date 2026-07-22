import pytest


# BUGS.md API-2: creating a resource should return 201, not 200.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-2: order creation returns 200 instead of 201", strict=True)
def test_create_order_returns_201(customer_client):
    resp = customer_client.create_order([{"product_id": 1, "quantity": 1}])

    assert resp.status_code == 201

    order_id = resp.json()["order"]["id"]
    customer_client.cancel_order(order_id)


def test_create_order_with_unknown_product_returns_400(customer_client):
    resp = customer_client.create_order([{"product_id": 999999, "quantity": 1}])

    assert resp.status_code == 400


def test_create_order_requires_a_bearer_token(anon_client):
    resp = anon_client.create_order([{"product_id": 1, "quantity": 1}])

    assert resp.status_code == 401


def test_customer_cannot_view_another_customers_order(customer_client, new_api_user):
    place_resp = customer_client.create_order([{"product_id": 1, "quantity": 1}])
    order_id = place_resp.json()["order"]["id"]

    other_client, _ = new_api_user
    resp = other_client.get_order(order_id)

    assert resp.status_code == 403

    customer_client.cancel_order(order_id)
