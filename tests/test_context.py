import platform
from unittest import TestCase

from alma_client import Client
from alma_client.version import __version__ as alma_version


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
            f"alma-client/{alma_version}; Python/{platform.python_version()}"
        )

    def test_context_exposes_credentials(self):
        assert self.context.credentials
