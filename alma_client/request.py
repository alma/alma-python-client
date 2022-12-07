import json
from typing import Optional

import httpx

from .paginated_results import PaginatedResults


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
        self.response_processor = lambda x: True

    def set_body(self, value):
        self.body = value
        return self

    def set_query_params(self, params):
        if not params:
            return
        self.params = params
        return self

    def expect(self, response_processor):
        self.response_processor = response_processor
        return self

    def expectJson(self, cls):
        self.response_processor = lambda response: cls(response.json)
        return self

    def expectPaginatedList(self, cls, next_page):
        self.response_processor = lambda response: PaginatedResults(response.json, cls, next_page)
        return self

    def get(self):
        self.method = "GET"
        return self

    def post(self):
        self.method = "POST"
        return self

    def put(self):
        self.method = "PUT"
        return self

    def delete(self):
        self.method = "DELETE"
        return self

    @property
    def data(self) -> Optional[bytes]:
        return json.dumps(self.body).encode("utf-8") if self.body is not None else None

    def to_httpx(self):
        self.context.credentials.configure(self)
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        req = httpx.Request(
            self.method,
            self.url,
            headers=headers,
            cookies=self.cookies,
            params=self.params,
            content=self.data,
        )
        return req
