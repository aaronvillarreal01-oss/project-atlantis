from datetime import date
from decimal import Decimal

from examples.intake.project_atlantis.core.models import (
    Invoice,
    InvoiceLine,
    InvoiceTotals,
    Party,
    Tax,
)


supplier = Party(
    name="Atlantis Supplier Ltd.",
    tax_id="12345678000199",
    country_code="BR",
)

customer = Party(
    name="Atlantis Customer S.A.",
    tax_id="98765432000188",
    country_code="BR",
)

vat_tax = Tax(
    tax_type="ICMS",
    tax_rate=Decimal("18.00"),
    taxable_amount=Decimal("1000.00"),
    tax_amount=Decimal("180.00"),
)

invoice_line = InvoiceLine(
    line_number="1",
    description="Tax technology consulting service",
    quantity=Decimal("1"),
    unit_price=Decimal("1000.00"),
    line_total=Decimal("1000.00"),
    classification_code="8471.30.12",
    taxes=[vat_tax],
)

invoice = Invoice(
    invoice_number="ATL-0001",
    issue_date=date.today(),
    currency_code="BRL",
    supplier=supplier,
    customer=customer,
    lines=[invoice_line],
    totals=InvoiceTotals(
        subtotal=Decimal("1000.00"),
        tax_total=Decimal("180.00"),
        grand_total=Decimal("1180.00"),
    ),
    source_format="NF-e",
)

print("Invoice created successfully")
print(f"Invoice number: {invoice.invoice_number}")
print(f"Supplier: {invoice.supplier.name}")
print(f"Customer: {invoice.customer.name}")
print(f"Grand total: {invoice.currency_code} {invoice.totals.grand_total}")