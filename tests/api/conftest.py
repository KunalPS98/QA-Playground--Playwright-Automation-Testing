import pytest

from api.client import QAPlaygroundApiClient
from utils.test_data import SAMPLE_ADMIN, SAMPLE_CUSTOMER, new_user_payload


@pytest.fixture
def anon_client(base_url) -> QAPlaygroundApiClient:
    return QAPlaygroundApiClient(base_url)


@pytest.fixture
def admin_client(base_url) -> QAPlaygroundApiClient:
    client = QAPlaygroundApiClient(base_url)
    client.login_as(SAMPLE_ADMIN["email"], SAMPLE_ADMIN["password"])
    return client


@pytest.fixture
def customer_client(base_url) -> QAPlaygroundApiClient:
    client = QAPlaygroundApiClient(base_url)
    client.login_as(SAMPLE_CUSTOMER["email"], SAMPLE_CUSTOMER["password"])
    return client


@pytest.fixture
def new_api_user(base_url, admin_client):
    payload = new_user_payload()
    client = QAPlaygroundApiClient(base_url)
    resp = client.register(payload["name"], payload["email"], payload["password"])
    body = resp.json()
    client.set_token(body["token"])

    yield client, body["user"]

    admin_client.delete_user(body["user"]["id"])


@pytest.fixture
def created_products(admin_client):
    created_ids = []

    def _create(**payload):
        resp = admin_client.create_product(**payload)
        if resp.status_code == 201:
            created_ids.append(resp.json()["product"]["id"])
        return resp

    yield _create

    for product_id in created_ids:
        admin_client.delete_product(product_id)
