from functools import wraps

from .paginated_results import PaginatedResults


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

    @configure_credentials
    def get(self):
        self.method = "GET"
        return self

    @configure_credentials
    def post(self):
        self.method = "POST"
        return self

    @configure_credentials
    def put(self):
        self.method = "PUT"
        return self

    @configure_credentials
    def delete(self):
        self.method = "DELETE"
        return self
