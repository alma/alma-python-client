from . import Credentials


class MerchantIdCredentials(Credentials):
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    def configure(self, request):
        request.headers["Authorization"] = "Alma-Merchant-Auth {merchant_id}".format(
            merchant_id=self.merchant_id
        )
