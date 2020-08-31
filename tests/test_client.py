import platform
from unittest import TestCase

import pytest
from unittest import mock
from alma import ApiModes, Client
from alma.credentials import ApiKeyCredentials, MerchantIdCredentials, AlmaSessionCredentials
from alma.request import Request
from alma.version import __version__ as alma_version


class ClientTest(TestCase):
    def test_client_raises_with_no_api_key_arguments_nor_credentials(self):
        with pytest.raises(ValueError, match=r"Valid credentials are required"):
            Client()

    def test_client_raises_with_empty_api_key_value(self):
        with pytest.raises(ValueError, match=r"Valid credentials are required"):
            Client(api_key="")

    def test_client_raises_with_empty_api_key_set_to_None(self):
        with pytest.raises(ValueError, match=r"Valid credentials are required"):
            Client(api_key=None)

    def test_client_detects_mode_with_regards_to_the_suggested_key(self):
        alma_client = Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
        assert alma_client.context.options["mode"] == ApiModes.LIVE
        alma_client = Client(api_key="sk_test_l6C92m3mqmS0aWcscEw62Xk4")
        assert alma_client.context.options["mode"] == ApiModes.TEST

    def test_client_inits_api_key_credentials_with_legacy_constructor(self):
        api_key = "sk_live_3geNR4OVI0gQGCAKgcYqQs2I"
        alma_client = Client(api_key=api_key)
        assert alma_client.context.credentials
        assert isinstance(alma_client.context.credentials, ApiKeyCredentials)
        assert alma_client.context.credentials.api_key == api_key

    def test_client_inits_api_key_credentials(self):
        api_key = "sk_live_3geNR4OVI0gQGCAKgcYqQs2I"
        alma_client = Client.with_api_key(api_key)

        assert alma_client.context.credentials
        assert isinstance(alma_client.context.credentials, ApiKeyCredentials)
        assert alma_client.context.credentials.api_key == api_key

    def test_client_inits_merchant_id_credentials(self):
        merchant_id = "merchant"
        alma_client = Client.with_merchant_id(merchant_id)

        assert alma_client.context.credentials
        assert isinstance(alma_client.context.credentials, MerchantIdCredentials)
        assert alma_client.context.credentials.merchant_id == merchant_id

    def test_client_inits_merchant_id_credentials(self):
        session_id = "merchant"
        cookie_name = "session_cookie"
        alma_client = Client.with_alma_session(session_id=session_id, cookie_name=cookie_name)

        assert alma_client.context.credentials
        assert isinstance(alma_client.context.credentials, AlmaSessionCredentials)
        assert alma_client.context.credentials.session_id == session_id
        assert alma_client.context.credentials.cookie_name == cookie_name

    def test_client_can_override_api_root_with_a_string(self):
        api_root = "http://localhost"
        alma_client = Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I", api_root=api_root)
        assert alma_client.context.options["api_root"] == {
            ApiModes.LIVE: api_root,
            ApiModes.TEST: api_root,
        }

    def test_client_can_override_api_root_with_a_dict(self):
        api_root = "http://localhost"
        alma_client = Client(
            api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I", api_root={ApiModes.LIVE: api_root}
        )
        assert alma_client.context.options["api_root"] == {
            ApiModes.LIVE: api_root,
        }

    def test_client_cannot_override_api_root_with_something_else(self):
        with pytest.raises(ValueError, match=r"`api_root` option must be a dict or a string"):
            Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I", api_root=12)

    def test_client_cannot_override_mode_with_something_else(self):
        with pytest.raises(ValueError, match=r"`mode` option must be one of \(live, test\)"):
            Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I", mode="blah")

    def test_client_expose_endpoints(self):
        alma_client = Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
        assert alma_client.payments.fetch_all
        assert alma_client.orders.fetch_all
        assert alma_client.exports.fetch_all

        # Exposed but empty
        assert alma_client.merchants


class ContextTest(TestCase):
    def setUp(self):
        client = Client.with_api_key("sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
        self.context = client.context

    def test_context_expose_logger(self):
        assert self.context.logger.name == "alma-python-client"
        assert self.context.logger.level == 0

    def test_context_expose_api_root_and_mode(self):
        assert self.context.api_root == self.context.options["api_root"]
        assert self.context.mode == self.context.options["mode"]

    def test_context_expose_url_for(self):
        assert self.context.url_for("/path/test") == "https://api.getalma.eu/path/test"

    def test_context_expose_user_agent_string(self):
        assert self.context.user_agent_string().startswith(
            "alma-client/{alma_version}; Python/{python_version}".format(
                alma_version=alma_version, python_version=platform.python_version()
            )
        )

    def test_context_exposes_credentials(self):
        assert self.context.credentials


class RequestTest(TestCase):
    def setUp(self) -> None:
        client = Client.with_api_key("sk_test_3geNR4OVI0gQGCAKgcYqQs2I")
        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def assert_method_calls_configure(self, method):
        with mock.patch(
            "alma.credentials.ApiKeyCredentials.configure"
        ) as mocked_configure, mock.patch("alma.request.requests"):
            getattr(self.request, method)()
            mocked_configure.assert_called_once_with(self.request)

    def test_credentials_configure_is_called_on_get(self):
        self.assert_method_calls_configure("get")

    def test_credentials_configure_is_called_on_post(self):
        self.assert_method_calls_configure("post")

    def test_credentials_configure_is_called_on_put(self):
        self.assert_method_calls_configure("put")


class ApiKeyCredentialsTest(TestCase):
    def setUp(self) -> None:
        self.api_key = "sk_test_3geNR4OVI0gQGCAKgcYqQs2I"
        client = Client.with_api_key(self.api_key)

        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_it_adds_authentication_header(self):
        self.credentials.configure(self.request)
        assert "Authorization" in self.request.headers
        assert self.request.headers["Authorization"] == "Alma-Auth {api_key}".format(
            api_key=self.api_key
        )


class MerchantIdCredentialsTest(TestCase):
    def setUp(self) -> None:
        self.merchant_id = "merchant"
        client = Client.with_merchant_id(self.merchant_id)

        self.credentials = client.context.credentials
        self.request = Request(client.context, "https://url.com")

    def test_it_adds_authentication_header(self):
        self.credentials.configure(self.request)

        assert "Authorization" in self.request.headers
        assert self.request.headers["Authorization"] == "Alma-Merchant-Auth {merchant_id}".format(
            merchant_id=self.merchant_id
        )


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
