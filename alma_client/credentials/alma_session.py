from .. import ApiModes
from .base import Credentials


class AlmaSessionCredentials(Credentials):
    def __init__(self, mode: ApiModes, session_id: str, cookie_name: str):
        super().__init__(mode)
        self.session_id = session_id
        self.cookie_name = cookie_name

    def configure(self, request):
        request.cookies[self.cookie_name] = self.session_id
