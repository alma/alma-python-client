from unittest import TestCase

from alma_client import Client
from alma_client.request import Request


class ApiKeyCredentialsTest(TestCase):
    def setUp(self) -> None:
        self.api_key = "sk_test_3geNR4OVI0gQGCAKgcYqQs2I"
        client = Client.with_api_key(self.api_key)

        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_it_adds_authentication_header(self):
        self.credentials.configure(self.request)
        assert "Authorization" in self.request.headers
        assert self.request.headers["Authorization"] == f"Alma-Auth {self.api_key}"


class MerchantIdCredentialsTest(TestCase):
    def setUp(self) -> None:
        self.merchant_id = "merchant"
        client = Client.with_merchant_id(self.merchant_id)

        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_it_adds_authentication_header(self):
        self.credentials.configure(self.request)

        assert "Authorization" in self.request.headers
        assert self.request.headers["Authorization"] == f"Alma-Merchant-Auth {self.merchant_id}"


class AlmaSessionCredentialsTest(TestCase):
    def setUp(self) -> None:
        self.session_id = "1234567890"
        self.cookie_name = "alma_session"
        client = Client.with_alma_session(self.session_id, self.cookie_name)

        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_it_adds_authentication_header(self):
        self.credentials.configure(self.request)

        assert self.cookie_name in self.request.cookies
        assert self.request.cookies[self.cookie_name] == self.session_id
