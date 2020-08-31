from functools import wraps

import requests

from .response import Response


def configure_credentials(func):
    def decorator(f):
        @wraps(f)
        def decorated(request, *args, **kwargs):
            request.context.credentials.configure(request)
            return f(request, *args, **kwargs)

        return decorated

    return decorator(func)


class RequestError(Exception):
    def __init__(self, error, url, response):
        self.error = error
        self.url = url
        self.response = response


class Request:
    def __init__(self, context, url):
        self.context = context
        self.url = url

        self.headers = {
            "User-Agent": self.context.user_agent_string(),
            "Accept": "application/json",
        }
        self.cookies = {}
        self.params = {}
        self.body = None

    def set_body(self, value):
        self.body = value
        return self

    def set_query_params(self, params):
        if not params:
            return
        self.params = params
        return self

    @configure_credentials
    def get(self):
        res = requests.get(self.url, self.params, headers=self.headers, cookies=self.cookies)
        return self._process_response(res)

    @configure_credentials
    def post(self):
        res = requests.post(self.url, json=self.body, headers=self.headers, cookies=self.cookies)
        return self._process_response(res)

    @configure_credentials
    def put(self):
        res = requests.put(self.url, json=self.body, headers=self.headers, cookies=self.cookies)
        return self._process_response(res)

    def _process_response(self, resp):
        response = Response(resp)

        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            if response.is_json() and "message" in response.json:
                error = response.json["message"]
            elif response.is_json() and "error" in response.json:
                error = response.json["error"]
            else:
                error = e.strerror

            raise RequestError(error, self, response)

        return response
