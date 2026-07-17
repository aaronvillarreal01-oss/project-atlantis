from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class Party:
    name: str
    tax_id: str
    country_code: str | None = None


@dataclass
class Tax:
    tax_type: str
    tax_rate: Decimal | None = None
    taxable_amount: Decimal | None = None
    tax_amount: Decimal = Decimal("0.00")


@dataclass
class InvoiceLine:
    line_number: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    line_total: Decimal
    classification_code: str | None = None
    taxes: list[Tax] = field(default_factory=list)


@dataclass
class InvoiceTotals:
    subtotal: Decimal
    tax_total: Decimal
    grand_total: Decimal


@dataclass
class Invoice:
    invoice_number: str
    issue_date: date | None
    currency_code: str
    supplier: Party
    customer: Party
    lines: list[InvoiceLine] = field(default_factory=list)
    totals: InvoiceTotals | None = None
    source_format: str | None = None