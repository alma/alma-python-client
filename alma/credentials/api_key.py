from . import Credentials


class ApiKeyCredentials(Credentials):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def configure(self, request):
        request.headers = {
            **request.headers,
            "Authorization": "Alma-Auth {api_key}".format(api_key=self.api_key),
        }
