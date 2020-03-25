import platform
from unittest import TestCase

import pytest
from alma import ApiModes, Client
from alma.version import __version__ as alma_version


class ClientTest(TestCase):
    def test_client_raises_with_no_api_key_arguments(self):
        with pytest.raises(
            TypeError, match=r"__init__\(\) missing 1 required positional argument: 'api_key'"
        ):
            Client()

    def test_client_raises_with_empty_api_key_value(self):
        with pytest.raises(ValueError, match=r"An API key is required"):
            Client(api_key="")

    def test_client_raises_with_empty_api_key_set_to_None(self):
        with pytest.raises(ValueError, match=r"An API key is required"):
            Client(api_key=None)

    def test_client_detects_mode_with_regards_to_the_suggested_key(self):
        alma_client = Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
        assert alma_client.context.options["mode"] == ApiModes.LIVE
        alma_client = Client(api_key="sk_test_l6C92m3mqmS0aWcscEw62Xk4")
        assert alma_client.context.options["mode"] == ApiModes.TEST

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
        client = Client(api_key="sk_live_3geNR4OVI0gQGCAKgcYqQs2I")
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
