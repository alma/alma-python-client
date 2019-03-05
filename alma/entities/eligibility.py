from .base import Base


class Eligibility(Base):
    @property
    def is_eligible(self):
        return self.eligible
