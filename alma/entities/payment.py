from enum import Enum

from .base import Base
from .installment import Installment
from .order import Order
from .refund import Refund


class PaymentState(Enum):
    # Payment has been created but its payment plan is not yet initialized
    NOT_READY = "not_ready"
    # Payment was just created, not scored and nothing paid yet
    NOT_STARTED = "not_started"
    # Was scored and not accepted
    SCORED_NO = "scored_no"
    # Was scored and not accepted - we need more data to improve scoring
    SCORED_MAYBE = "scored_maybe"
    # Was scored and accepted
    SCORED_YES = "scored_yes"

    # After SCORED_YES, the first installment has been paid
    IN_PROGRESS = "in_progress"
    # Payment fully done
    PAID = "paid"

    # No more installments will be taken from this payment
    STOPPED = "stopped"

    # Problem with payment, potential default
    # Next installment is not paid and was due in the past (less than 7 days ago)
    # retrying to charge the card regularly
    LATE_DUNNING = "late_dunning"
    # Next installment is very late, between 8 and 15 days. Contacting customer with email and SMS
    LATE_CONTACT_CUSTOMER = "late_contact_customer"
    # More than 15 days late, payment is considered in default:
    # (i) claim is opened and (ii) payments switches to judiciary collection
    DEFAULT = "default"
    # After default, we may recover part of the payment through judiciary collection.
    # Once collection has been completed, this stage is reached and nothing happens anymore
    COLLECTION_DONE = "collection_done"


class PaymentFraudType(Enum):
    AMOUNT_MISMATCH = "amount_mismatch"
    STATE_ERROR = "state_error"


class Payment(Base):
    def __init__(self, data):
        payment_plan = data.pop("payment_plan", [])
        self.payment_plan = [Installment(d) for d in payment_plan]

        state = data.pop("state", None)
        if state:
            try:
                self.state = PaymentState(state)
            except ValueError:
                # Pass on unrecognized state values
                # restore it in the raw Payment data so that it can still be retrieved
                data["state"] = state

        orders = data.pop("orders", [])
        self.orders = [Order(o) for o in orders]

        refunds = data.pop("refunds", [])
        self.refunds = [Refund(r) for r in refunds]

        super(Payment, self).__init__(data)
