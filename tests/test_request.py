from unittest import TestCase, mock

from alma_client import Client
from alma_client.request import Request


class RequestTest(TestCase):
    def setUp(self) -> None:
        client = Client.with_api_key("sk_test_3geNR4OVI0gQGCAKgcYqQs2I")
        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_credentials_configure_is_called_on_request_build(self):
        with mock.patch("alma_client.credentials.ApiKeyCredentials.configure") as mocked_configure:
            self.request.get()
            mocked_configure.assert_not_called()
            # only upon building the httpx Req are the credentials configured
            _ = self.request.to_httpx()
            mocked_configure.assert_called_once_with(self.request)
