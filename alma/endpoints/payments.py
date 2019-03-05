from .base import Base
from alma.entities import Payment, Eligibility


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

    def fetch(self, payment_id):
        response = self.request(f"{self.PAYMENTS_PATH}/{payment_id}").get()
        return Payment(response.json)

    def flag_as_potential_fraud(self, payment_id, reason=None):
        request = self.request(f"{self.PAYMENTS_PATH}/{payment_id}/potential-fraud")

        if reason:
            request.set_body({"reason": reason})

        request.post()
        return True
