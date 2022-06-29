from enum import Enum

from alma_client.entities import Base


class FeePlanKind(Enum):
    GENERAL = "general"
    POS = "pos"


class FeePlan(Base):
    def __init__(self, data):
        kind = data.pop("kind", None)
        if kind:
            try:
                self.kind = FeePlanKind(kind)
            except ValueError:
                # Pass on unrecognized kind values
                # restore it in the raw Payment data so that it can still be retrieved
                data["kind"] = kind

        super(FeePlan, self).__init__(data)
