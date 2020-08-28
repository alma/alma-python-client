from ..entities import Merchant
from . import Base


class Merchants(Base):
    MERCHANTS_PATH = "/v1/merchants"
    ME_PATH = "/v1/me"
    EXTENDED_ME_PATH = "/v1/me/extended-data"

    def me(self, extended=False):
        response = self.request(self.EXTENDED_ME_PATH if extended else self.ME_PATH).get()

        return Merchant(response.json)

    def fetch(self, merchant_id):
        response = self.request(f"{self.MERCHANTS_PATH}/{merchant_id}").get()
        return Merchant(response.json)
