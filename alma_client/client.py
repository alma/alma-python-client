import logging
import platform
from functools import wraps
from typing import Dict, Optional

import httpx

from . import endpoints
from .api_modes import ApiModes
from .context import Context
from .credentials import (
    AlmaSessionCredentials,
    ApiKeyCredentials,
    Credentials,
    MerchantIdCredentials,
)
from .request import Request, RequestError
from .response import Response
from .version import __version__ as alma_version


def process_request(req):

    request = req.to_httpx()
    with httpx.Client() as client:
        resp = client.send(request)

    response = Response(resp)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if response.is_json() and "message" in response.json:
            error = response.json["message"]
        elif response.is_json() and "error" in response.json:
            error = response.json["error"]
        else:
            error = str(e)

        raise RequestError(error, req.url, response)

    return response


def request_processor(func):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            req = f(*args, **kwargs)
            if isinstance(req, Request):
                resp = process_request(req)
                response = req.response_processor(resp)
                if hasattr(response, "next_page"):
                    setattr(response, "next_page", request_processor(response.next_page))
                return response
            return req

        return decorated

    return decorator(func)


class EndpointHandler:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __getattr__(self, attr):
        method = getattr(self.endpoint, attr)
        return request_processor(method)


class Client:
    SANDBOX_API_URL = "https://api.sandbox.getalma.eu"
    LIVE_API_URL = "https://api.getalma.eu"

    @classmethod
    def with_api_key(cls, api_key: str, **options):
        return cls(credentials=ApiKeyCredentials(api_key), **options)

    @classmethod
    def with_merchant_id(cls, merchant_id: str, mode: ApiModes = ApiModes.LIVE, **options):
        return cls(credentials=MerchantIdCredentials(mode, merchant_id), **options)

    @classmethod
    def with_alma_session(
        cls,
        session_id: str,
        cookie_name: str = "alma_sess",
        mode: ApiModes = ApiModes.LIVE,
        **options,
    ):
        return cls(credentials=AlmaSessionCredentials(mode, session_id, cookie_name), **options)

    def __init__(
        self,
        api_key: Optional[str] = None,
        credentials: Optional[Credentials] = None,
        mode: Optional[ApiModes] = None,
        **kwargs,
    ):
        """
        Create a new instance of the Alma API Client.

        It is recommended to use one the convenience methods instead of the default constructor:
        - Client.with_api_key
        - Client.with_merchant_id
        - Client.with_alma_session

        :param  api_key:    Deprecated - use Client.with_api_key("<api_key>") instead
        :type   api_key:    str

        :param      credentials   A `Credentials` instance to be used to configure requests made to
                                the API. This would typically be set by one of the convenience
                                methods mentioned above.
        :type       credentials Credentials

        :param      mode        Deprecated. Use `mode` param of convenience methods above
                                API mode to be used: either ApiModes.LIVE or ApiModes.TEST
        :type       mode        ApiModes

        :keyword    logger      A logger instance to be used instead of the default one
        :keyword    api_root    root URL(s) to call Alma's API at.
                                You probably don't want to change it!

                                Expected types:
                                -------------
                                str: the provided URL will be used for both LIVE and TEST modes
                                dict: must have two keys, ApiModes.LIVE and ApiModes.TEST, each
                                      value must be the URL to be used for each mode

        """
        if isinstance(credentials, ApiKeyCredentials):
            api_key = credentials.api_key

        if not credentials:
            if not api_key:
                raise ValueError("Valid credentials are required to instantiate a new Client")

            # Backward compatibility with the older init method
            credentials = ApiKeyCredentials(api_key)

        options = {
            "api_root": {ApiModes.TEST: self.SANDBOX_API_URL, ApiModes.LIVE: self.LIVE_API_URL},
            "mode": mode if mode is not None else credentials.mode,
            "logger": logging.getLogger("alma-python-client"),
            "credentials": credentials,
            **kwargs,
        }

        if type(options["api_root"]) is str:
            options["api_root"] = {
                ApiModes.TEST: options["api_root"],
                ApiModes.LIVE: options["api_root"],
            }
        elif type(options["api_root"]) is not dict:
            raise ValueError("`api_root` option must be a dict or a string")

        if options["mode"] not in (ApiModes.LIVE, ApiModes.TEST):
            raise ValueError(
                f"`mode` option must be one of ({ApiModes.LIVE.value}, {ApiModes.TEST.value})"
            )

        self.context = Context(options)
        self.init_user_agent()
        self._endpoints: Dict[str, endpoints.Base] = {}

    def add_user_agent_component(self, component, version):
        self.context.add_user_agent_component(component, version)

    def init_user_agent(self):
        self.add_user_agent_component("Python", platform.python_version())
        self.add_user_agent_component("alma-client", alma_version)

    def _endpoint(self, endpoint_name):
        endpoint = self._endpoints.get(endpoint_name)

        if endpoint is None:
            endpoint = EndpointHandler(getattr(endpoints, endpoint_name)(self.context))
            self._endpoints[endpoint] = endpoint

        return endpoint

    @property
    def payments(self) -> endpoints.Payments:
        return self._endpoint("Payments")

    @property
    def merchants(self) -> endpoints.Merchants:
        return self._endpoint("Merchants")

    @property
    def orders(self) -> endpoints.Orders:
        return self._endpoint("Orders")

    @property
    def exports(self) -> endpoints.Exports:
        return self._endpoint("Exports")
