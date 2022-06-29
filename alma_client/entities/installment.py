from enum import Enum

from . import Base


class InstallmentState(Enum):
    PENDING = "pending"
    PAID = "paid"
    INCIDENT = "incident"
    CLAIMED = "claimed"
    COVERED = "covered"


class Installment(Base):
    def __init__(self, data):
        state = data.pop("state", None)
        if state:
            try:
                self.state = InstallmentState(state)
            except ValueError:
                # Pass on unrecognized state values
                # they will be accessible as-is in the Installment data
                pass

        super(Installment, self).__init__(data)
