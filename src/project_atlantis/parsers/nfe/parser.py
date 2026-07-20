from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import xml.etree.ElementTree as ET

from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.core.models import Invoice, InvoiceTotals, Party
from project_atlantis.parsers.base import BaseParser


NFE_NAMESPACE = "http://www.portalfiscal.inf.br/nfe"
NS = {"nfe": NFE_NAMESPACE}


class NFeParsingError(ValueError):
    """Raised when an NF-e document cannot be converted into an Invoice."""


class NFeParser(BaseParser):
    """Convert a Brazilian NF-e XML document into Atlantis's canonical model."""

    def parse(self, file_path: str | Path) -> Invoice:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Invoice file not found: {path}")

        try:
            tree = ET.parse(path)
        except ET.ParseError as exc:
            raise NFeParsingError(f"Invalid XML document: {path}") from exc

        root = tree.getroot()

        invoice_number = self._required_text(
            root,
            ".//nfe:ide/nfe:nNF",
        )

        issue_date = self._parse_issue_date(root)

        supplier = Party(
            name=self._required_text(
                root,
                ".//nfe:emit/nfe:xNome",
            ),
            tax_id=self._party_tax_id(
                root,
                ".//nfe:emit",
            ),
            country_code="BR",
        )

        customer = Party(
            name=self._required_text(
                root,
                ".//nfe:dest/nfe:xNome",
            ),
            tax_id=self._party_tax_id(
                root,
                ".//nfe:dest",
            ),
            country_code="BR",
        )

        totals = self._parse_totals(root)

        return Invoice(
            invoice_number=invoice_number,
            issue_date=issue_date,
            currency_code="BRL",
            supplier=supplier,
            customer=customer,
            totals=totals,
            source_format=InvoiceFormat.NFE,
        )

    @staticmethod
    def _required_text(root: ET.Element, xpath: str) -> str:
        element = root.find(xpath, NS)

        if element is None or not element.text or not element.text.strip():
            raise NFeParsingError(
                f"Required NF-e field not found: {xpath}"
            )

        return element.text.strip()

    def _party_tax_id(
        self,
        root: ET.Element,
        party_xpath: str,
    ) -> str:
        party = root.find(party_xpath, NS)

        if party is None:
            raise NFeParsingError(
                f"Required NF-e party not found: {party_xpath}"
            )

        for tag_name in ("CNPJ", "CPF", "idEstrangeiro"):
            element = party.find(
                f"nfe:{tag_name}",
                NS,
            )

            if element is not None and element.text and element.text.strip():
                return element.text.strip()

        raise NFeParsingError(
            f"No CNPJ, CPF, or foreign tax ID found for party: "
            f"{party_xpath}"
        )

    def _parse_issue_date(
        self,
        root: ET.Element,
    ) -> date | None:
        # NF-e 4.00 normally uses dhEmi.
        # Older documents may use dEmi.
        date_xpaths = (
            ".//nfe:ide/nfe:dhEmi",
            ".//nfe:ide/nfe:dEmi",
        )

        for xpath in date_xpaths:
            element = root.find(xpath, NS)

            if element is None:
                continue

            if not element.text or not element.text.strip():
                continue

            value = element.text.strip()

            try:
                return datetime.fromisoformat(value).date()
            except ValueError as exc:
                raise NFeParsingError(
                    f"Invalid NF-e issue date: {value}"
                ) from exc

        return None

    def _parse_totals(
        self,
        root: ET.Element,
    ) -> InvoiceTotals:
        subtotal = self._required_decimal(
            root,
            ".//nfe:total/nfe:ICMSTot/nfe:vProd",
        )

        grand_total = self._required_decimal(
            root,
            ".//nfe:total/nfe:ICMSTot/nfe:vNF",
        )

        tax_total = grand_total - subtotal

        return InvoiceTotals(
            subtotal=subtotal,
            tax_total=tax_total,
            grand_total=grand_total,
        )

    @staticmethod
    def _required_decimal(
        root: ET.Element,
        xpath: str,
    ) -> Decimal:
        element = root.find(xpath, NS)

        if element is None or not element.text or not element.text.strip():
            raise NFeParsingError(
                f"Required NF-e amount not found: {xpath}"
            )

        value = element.text.strip()

        try:
            return Decimal(value)
        except InvalidOperation as exc:
            raise NFeParsingError(
                f"Invalid NF-e monetary amount at {xpath}: {value}"
            ) from exc