from unittest import TestCase, mock

from alma_client import Client
from alma_client.request import Request


class RequestTest(TestCase):
    def setUp(self) -> None:
        client = Client.with_api_key("sk_test_3geNR4OVI0gQGCAKgcYqQs2I")
        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def assert_method_calls_configure(self, method):
        with mock.patch("alma_client.credentials.ApiKeyCredentials.configure") as mocked_configure:
            getattr(self.request, method)()
            mocked_configure.assert_called_once_with(self.request)

    def test_credentials_configure_is_called_on_get(self):
        self.assert_method_calls_configure("get")

    def test_credentials_configure_is_called_on_post(self):
        self.assert_method_calls_configure("post")

    def test_credentials_configure_is_called_on_put(self):
        self.assert_method_calls_configure("put")

    def test_credentials_configure_is_called_on_delete(self):
        self.assert_method_calls_configure("delete")
