from dataclasses import dataclass

from project_atlantis.core.enums import InvoiceFormat


@dataclass(frozen=True)
class InvoiceDetectionResult:
    """
    Result produced by the Invoice Intake Engine before parsing.
    """

    invoice_format: InvoiceFormat
    root_element: str
    namespace: str
    version: str | None = None
    country_code: str | None = None
    authority_system: str | None = None