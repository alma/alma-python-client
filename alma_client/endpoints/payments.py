from functools import partial
from typing import List, Union

from ..entities import Eligibility, Order, Payment
from . import Base


class Payments(Base):
    PAYMENTS_PATH = "/v1/payments"

    def eligibility(self, order_data):
        return (
            self.request(f"{self.PAYMENTS_PATH}/eligibility")
            .set_body(order_data)
            .post()
            .expect(
                lambda response: [Eligibility(i) for i in response.json]
                if isinstance(response.json, list)
                else Eligibility(response.json)
            )
        )

    def create(self, data):
        return self.request(self.PAYMENTS_PATH).set_body(data).post().expectJson(Payment)

    def update(self, payment_id, data):
        return (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}")
            .set_body(data)
            .post()
            .expectJson(Payment)
        )

    def fetch_all(self, limit: int = 20, states: list = None, starting_after: str = None):
        args = {"limit": str(limit)}
        if starting_after:
            args["starting_after"] = starting_after
        if states:
            args["state"] = ",".join(states)

        next_page = partial(self.fetch_all, limit=limit, states=states)
        return (
            self.request(self.PAYMENTS_PATH)
            .set_query_params(args)
            .get()
            .expectPaginatedList(Payment, next_page)
        )

    def fetch(self, payment_id=None, limit=20, states=None):
        if payment_id is None:
            return self.fetch_all(limit=limit, states=states)
        else:
            return self.request(f"{self.PAYMENTS_PATH}/{payment_id}").get().expectJson(Payment)

    def flag_as_potential_fraud(self, payment_id, reason=None):
        request = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/potential-fraud")

        if reason:
            request.set_body({"reason": reason})

        return request.post()

    def add_orders_to(self, payment_id, order_data: Union[List[dict], dict]) -> List[Order]:
        """
        Adds one or several orders to the given payment

        :param payment_id: ID of the payment to add the order(s) to
        :param order_data: Either a dict of attributes for a single order,
                           or a list of such dicts for several
        :return: List of Order instances that were added to the payment
        """
        if isinstance(order_data, dict):
            order_data = [order_data]

        return (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders")
            .set_body({"orders": order_data})
            .put()
            .expect(lambda response: [Order(o) for o in response.json])
        )

    def set_orders_for(self, payment_id, order_data: Union[List[dict], dict]) -> List[Order]:
        """
        Sets one or several orders on the given payment (replacing existing ones)

        :param payment_id: ID of the payment to add the order(s) to
        :param order_data: Either a dict of attributes for a single order,
                           or a list of such dicts for several
        :return: List of Order instances that were added to the payment
        """
        if isinstance(order_data, dict):
            order_data = [order_data]

        return (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders")
            .set_body({"orders": order_data})
            .post()
            .expect(lambda response: [Order(o) for o in response.json])
        )

    def get_orders_for(self, payment_id) -> List[Order]:
        return (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/orders")
            .get()
            .expect(lambda response: [Order(o) for o in response.json])
        )

    def ask_acceptance(self, payment_id: str) -> Payment:
        return (
            self.request(f"{self.PAYMENTS_PATH}/{payment_id}/ask-acceptance")
            .get()
            .expectJson(Payment)
        )

    def charge_first_installment(self, payment_id: str, data) -> Payment:
        req = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/charge-first-installment")

        req.set_body(data)

        return req.post().expectJson(Payment)

    def refund(self, payment_id: str, amount: int, full_refund: bool = False, **params) -> Payment:
        """
        Refunds given payment of the given amount (in cents).
        If `full_refund` is `True`, `amount` is ignored
        to trigger a full refund of the payment, including potential customer fees.

        :param payment_id: ID of the payment to refund
        :param amount: Amount, in cents, to be refunded on the payment
        :param full_refund: True if the full payment should be refunded (with customer fees).
                            Default: false.
        :return: Updated payment object
        """
        req = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/refund")

        refund_params = {}
        if not full_refund:
            refund_params["amount"] = amount

        req.set_body({**params, **refund_params})

        return req.post().expectJson(Payment)

    def send_sms(self, payment_id: str):
        """
        Sends a payment link via SMS, to the customer's saved mobile phone number.

        Will raise RequestError if the SMS API is not activated on your account or
        in case of any other error, otherwise returns True.
        """
        return self.request(f"{self.PAYMENTS_PATH}/{payment_id}/send-sms").post()
