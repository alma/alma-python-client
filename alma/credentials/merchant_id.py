from .. import ApiModes
from .base import Credentials


class MerchantIdCredentials(Credentials):
    def __init__(self, mode: ApiModes, merchant_id: str):
        super().__init__(mode)
        self.merchant_id = merchant_id

    def configure(self, request):
        request.headers["Authorization"] = "Alma-Merchant-Auth {merchant_id}".format(
            merchant_id=self.merchant_id
        )
