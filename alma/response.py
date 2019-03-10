class Response:
    def __init__(self, resp):
        self.resp = resp

    def is_json(self):
        try:
            self.resp.json()
        except Exception:
            return False

        return True

    @property
    def status_code(self):
        return self.resp.status_code

    @property
    def json(self):
        return self.resp.json()
