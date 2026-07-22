import requests


class QAPlaygroundApiClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/") + "/api"
        self.session = requests.Session()
        self.token = None
        if token:
            self.set_token(token)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def set_token(self, token: str):
        self.token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    # auth

    def register(self, name: str, email: str, password: str) -> requests.Response:
        return self.session.post(self._url("/auth/register"), json={"name": name, "email": email, "password": password})

    def login(self, email: str, password: str) -> requests.Response:
        return self.session.post(self._url("/auth/login"), json={"email": email, "password": password})

    def login_as(self, email: str, password: str) -> requests.Response:
        response = self.login(email, password)
        token = response.json().get("token")
        if token:
            self.set_token(token)
        return response

    def me(self) -> requests.Response:
        return self.session.get(self._url("/auth/me"))

    # products

    def list_products(self, **params) -> requests.Response:
        return self.session.get(self._url("/products"), params=params)

    def get_product(self, product_id) -> requests.Response:
        return self.session.get(self._url(f"/products/{product_id}"))

    def create_product(self, **payload) -> requests.Response:
        return self.session.post(self._url("/products"), json=payload)

    def update_product(self, product_id, **payload) -> requests.Response:
        return self.session.put(self._url(f"/products/{product_id}"), json=payload)

    def delete_product(self, product_id) -> requests.Response:
        return self.session.delete(self._url(f"/products/{product_id}"))

    # orders

    def create_order(self, items: list) -> requests.Response:
        return self.session.post(self._url("/orders"), json={"items": items})

    def list_orders(self) -> requests.Response:
        return self.session.get(self._url("/orders"))

    def get_order(self, order_id) -> requests.Response:
        return self.session.get(self._url(f"/orders/{order_id}"))

    def cancel_order(self, order_id) -> requests.Response:
        return self.session.post(self._url(f"/orders/{order_id}/cancel"))

    # users

    def get_user(self, user_id) -> requests.Response:
        return self.session.get(self._url(f"/users/{user_id}"))

    def list_users(self) -> requests.Response:
        return self.session.get(self._url("/users"))

    def delete_user(self, user_id) -> requests.Response:
        return self.session.delete(self._url(f"/users/{user_id}"))
