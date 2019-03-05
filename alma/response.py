class Response:
    def __init__(self, resp):
        self.resp = resp

    @property
    def status_code(self):
        return self.resp.status_code

    @property
    def json(self):
        return self.resp.json()
