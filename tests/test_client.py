from unittest import TestCase

import pytest

from alma_client import ApiModes, Client
from alma_client.credentials import AlmaSessionCredentials, ApiKeyCredentials, MerchantIdCredentials


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

    def test_client_inits_with_cookies_credentials(self):
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
