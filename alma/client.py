import logging
import platform

from . import __version__ as alma_version, endpoints
from .api_modes import ApiMode
from .context import Context


class Client:
    SANDBOX_API_URL = "https://api.sandbox.getalma.eu"
    LIVE_API_URL = "https://api.getalma.eu"

    def __init__(self, api_key, **options):
        if not api_key:
            raise ValueError("An API key is required to instantiate a new Client")

        options = {
            "api_root": {
                ApiMode.TEST: self.SANDBOX_API_URL,
                ApiMode.LIVE: self.LIVE_API_URL,
            },
            "mode": ApiMode.LIVE,
            "logger": logging.getLogger("alma-python-client"),
            **options,
        }

        if type(options["api_root"]) is str:
            options["api_root"] = {
                ApiMode.TEST: options["api_root"],
                ApiMode.LIVE: options["api_root"],
            }
        elif type(options["api_root"]) is not dict:
            raise TypeError("`api_root` option must be a dict or a string")

        if options["mode"] not in (ApiMode.LIVE, ApiMode.TEST):
            raise ValueError(
                f"`mode` option must be one of ({ApiMode.LIVE}, {ApiMode.TEST})"
            )

        self.context = Context(api_key, options)

        self.init_user_agent()
        self.init_endpoints()

    def add_user_agent_component(self, component, version):
        self.context.add_user_agent_component(component, version)

    def init_user_agent(self):
        self.add_user_agent_component("Python", platform.python_version())
        self.add_user_agent_component("Alma for Python", alma_version)

    def init_endpoints(self):
        self.payments = endpoints.Payments(self.context)
        self.merchants = endpoints.Merchants(self.context)
