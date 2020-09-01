from alma import ApiModes
from alma.request import Request


class Credentials:
    def __init__(self, mode: ApiModes):
        self._mode = mode

    def configure(self, request: Request):
        raise NotImplementedError()

    @property
    def mode(self):
        return self._mode
