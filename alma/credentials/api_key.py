from .. import ApiModes
from .base import Credentials


class ApiKeyCredentials(Credentials):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super().__init__(self.mode)

    def configure(self, request):
        request.headers["Authorization"] = f"Alma-Auth {self.api_key}"

    @property
    def mode(self):
        return ApiModes.LIVE if self.api_key.startswith("sk_live") else ApiModes.TEST
