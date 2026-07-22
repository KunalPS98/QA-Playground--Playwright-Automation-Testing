import pytest


def test_users_list_requires_admin(customer_client):
    resp = customer_client.list_users()

    assert resp.status_code == 403


def test_admin_can_list_users(admin_client):
    resp = admin_client.list_users()

    assert resp.status_code == 200
    assert all("password_hash" not in user for user in resp.json()["users"])


# BUGS.md API-7: the single-user endpoint leaks password_hash, unlike the
# list endpoint above which correctly strips it.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-7: user detail response exposes password_hash", strict=True)
def test_user_detail_hides_password_hash(new_api_user):
    client, user = new_api_user

    resp = client.get_user(user["id"])

    assert "password_hash" not in resp.json()["user"]
