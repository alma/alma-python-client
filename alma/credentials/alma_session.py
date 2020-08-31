from . import Credentials


class AlmaSessionCredentials(Credentials):
    def __init__(self, session_id: str, cookie_name: str):
        self.session_id = session_id
        self.cookie_name = cookie_name

    def configure(self, request):
        request.cookies = {**request.cookies, self.cookie_name: self.session_id}
