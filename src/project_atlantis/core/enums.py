from enum import Enum


class InvoiceFormat(str, Enum):
    NFE = "NFE"
    UBL = "UBL"
    CFDI = "CFDI"
    UNKNOWN = "UNKNOWN"