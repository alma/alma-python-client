from typing import List, Optional

from ..entities import FeePlan, FeePlanKind, Merchant
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

    def fee_plans(self, kind: FeePlanKind, only: Optional[List[int]] = None):
        params = {"kind": kind.value}

        if only is not None:
            params["only"] = ",".join(str(i) for i in only)

        return (
            self.request(f"{self.ME_PATH}/fee-plans")
            .set_query_params(params)
            .get()
            .expect(lambda resp: [FeePlan(fp) for fp in resp.json])
        )

    def fetch(self, merchant_id):
        response = self.request(f"{self.MERCHANTS_PATH}/{merchant_id}").get()
        return Merchant(response.json)
