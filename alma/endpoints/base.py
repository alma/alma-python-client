from ..request import Request


class Base:
    def __init__(self, context):
        self.endpoint = self
        self.context = context

    @property
    def logger(self):
        return self.context.logger

    def request(self, path):
        return Request(self.context, self.context.url_for(path))
