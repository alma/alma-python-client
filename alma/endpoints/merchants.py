from ..entities import Merchant
from . import Base


class Merchants(Base):
    MERCHANTS_PATH = "/v1/merchants"
    ME_PATH = "/v1/me"
    EXTENDED_ME_PATH = "/v1/me/extended-data"

    def me(self, extended=False):
        return (
            self.request(self.EXTENDED_ME_PATH if extended else self.ME_PATH)
            .get()
            .expectJson(Merchant)
        )
