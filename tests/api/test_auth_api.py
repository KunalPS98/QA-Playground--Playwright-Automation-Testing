import pytest

from api.client import QAPlaygroundApiClient
from utils.test_data import SAMPLE_CUSTOMER, new_user_payload


def test_register_creates_a_new_user(base_url, admin_client):
    payload = new_user_payload()
    client = QAPlaygroundApiClient(base_url)

    resp = client.register(payload["name"], payload["email"], payload["password"])

    assert resp.status_code == 201
    body = resp.json()
    assert body["user"]["email"] == payload["email"]
    assert "token" in body

    admin_client.delete_user(body["user"]["id"])


def test_login_with_valid_credentials_returns_a_token(anon_client):
    resp = anon_client.login(SAMPLE_CUSTOMER["email"], SAMPLE_CUSTOMER["password"])

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["token"]


# BUGS.md API-1: invalid credentials return 200 with success:false instead
# of a proper 401.
@pytest.mark.bug
@pytest.mark.xfail(reason="API-1: invalid login returns 200 instead of 401", strict=True)
def test_login_with_invalid_password_returns_401(anon_client):
    resp = anon_client.login(SAMPLE_CUSTOMER["email"], "wrong-password")

    assert resp.status_code == 401


def test_me_requires_a_bearer_token(anon_client):
    resp = anon_client.me()

    assert resp.status_code == 401
