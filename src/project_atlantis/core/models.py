from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from project_atlantis.core.enums import InvoiceFormat


@dataclass
class Party:
    """Represents a supplier, customer, or any invoice party."""

    name: str
    tax_id: str
    country_code: str | None = None


@dataclass
class Tax:
    """Represents a tax applied to an invoice or invoice line."""

    tax_type: str
    tax_rate: Decimal | None = None
    taxable_amount: Decimal | None = None
    tax_amount: Decimal = Decimal("0.00")


@dataclass
class InvoiceLine:
    """Represents a single invoice line."""

    line_number: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    line_total: Decimal
    product_classification: str | None = None
    taxes: list[Tax] = field(default_factory=list)


@dataclass
class InvoiceTotals:
    """Represents invoice totals."""

    subtotal: Decimal
    tax_total: Decimal
    grand_total: Decimal


@dataclass
class Invoice:
    """Canonical invoice model used across all supported formats."""

    invoice_number: str
    issue_date: date | None
    currency_code: str
    supplier: Party
    customer: Party
    lines: list[InvoiceLine] = field(default_factory=list)
    totals: InvoiceTotals | None = None
    source_format: InvoiceFormat = InvoiceFormat.UNKNOWN