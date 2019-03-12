from functools import partial
from typing import Union, List

from . import Base
from ..entities import Payment, Eligibility, Order
from ..paginated_results import PaginatedResults


class Payments(Base):
    PAYMENTS_PATH = "/v1/payments"

    def eligibility(self, order_data):
        response = (
            self.request(f"{self.PAYMENTS_PATH}/eligibility")
            .set_body(order_data)
            .post()
        )

        return Eligibility(response.json)

    def create(self, data):
        response = self.request(self.PAYMENTS_PATH).set_body(data).post()
        return Payment(response.json)

    def fetch_all(self, limit=20, starting_after=None):
        args = {"limit": limit}
        if starting_after:
            args["starting_after"] = starting_after

        response = self.request(self.PAYMENTS_PATH).set_query_params(args).get()

        next_page = partial(self.fetch_all, limit=limit)
        return PaginatedResults(response.json, Payment, next_page)

    def fetch(self, payment_id=None, limit=20):
        if payment_id is None:
            return self.fetch_all(limit)
        else:
            response = self.request(f"{self.PAYMENTS_PATH}/{payment_id}").get()
            return Payment(response.json)

    def flag_as_potential_fraud(self, payment_id, reason=None):
        request = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/potential-fraud")

        if reason:
            request.set_body({"reason": reason})

        request.post()
        return True

    def add_orders_to(
        self, payment_id, order_data: Union[List[dict], dict]
    ) -> List[Order]:
        """
        Adds one or several orders to the given payment

        :param payment_id: ID of the payment to add the order(s) to
        :param order_data: Either a dict of attributes for a single order, or a list of such dicts for several
        :return: List of Order instances that were added to the payment
        """
        if type(order_data) is dict:
            order_data = [order_data]

        response = (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders")
            .set_body({"orders": order_data})
            .put()
        )

        return [Order(o) for o in response.json]

    def set_orders_for(
        self, payment_id, order_data: Union[List[dict], dict]
    ) -> List[Order]:
        """
        Sets one or several orders on the given payment (replacing existing ones)

        :param payment_id: ID of the payment to add the order(s) to
        :param order_data: Either a dict of attributes for a single order, or a list of such dicts for several
        :return: List of Order instances that were added to the payment
        """
        if type(order_data) is dict:
            order_data = [order_data]

        response = (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders")
            .set_body({"orders": order_data})
            .post()
        )

        return [Order(o) for o in response.json]

    def get_orders_for(self, payment_id) -> List[Order]:
        response = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders").get()
        return [Order(o) for o in response.json]
