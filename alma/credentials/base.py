from alma.request import Request


class Credentials:
    def configure(self, request: Request):
        raise NotImplementedError()
