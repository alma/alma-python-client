from enum import Enum

from . import Base


class ExportType(Enum):
    PAYMENTS = "payments"
    ACCOUNTING = "accounting"
    ACCOUNTING_FOR_PAYOUT = "accounting_for_payout"


class ExportFormat(Enum):
    CSV = "csv"
    PDF = "pdf"
    XLSX = "xlsx"


class Export(Base):
    pass
