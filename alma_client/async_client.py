from functools import wraps

import httpx

from . import endpoints
from .client import Client
from .request import Request, RequestError
from .response import Response


async def process_request(req):

    request = req.to_httpx()
    async with httpx.AsyncClient() as client:
        resp = await client.send(request)

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
        async def decorated(*args, **kwargs):
            req = f(*args, **kwargs)
            if isinstance(req, Request):
                resp = await process_request(req)
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


class AsyncClient(Client):
    def _endpoint(self, endpoint_name):
        endpoint = self._endpoints.get(endpoint_name)

        if endpoint is None:
            endpoint = EndpointHandler(getattr(endpoints, endpoint_name)(self.context))
            self._endpoints[endpoint] = endpoint

        return endpoint
