from datetime import date
from pathlib import Path

import pytest

from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.parsers.nfe import NFeParser, NFeParsingError


VALID_NFE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
    <infNFe Id="NFe123" versao="4.00">
        <ide>
            <nNF>12345</nNF>
            <dhEmi>2026-07-19T09:30:00-03:00</dhEmi>
        </ide>

        <emit>
            <CNPJ>12345678000199</CNPJ>
            <xNome>ABC Manufacturing Ltda.</xNome>
        </emit>

        <dest>
            <CPF>12345678901</CPF>
            <xNome>Customer Example</xNome>
        </dest>
    </infNFe>
</NFe>
"""


def test_nfe_parser_creates_canonical_invoice(tmp_path: Path):
    xml_file = tmp_path / "invoice.xml"
    xml_file.write_text(VALID_NFE_XML, encoding="utf-8")

    invoice = NFeParser().parse(xml_file)

    assert invoice.invoice_number == "12345"
    assert invoice.issue_date == date(2026, 7, 19)
    assert invoice.currency_code == "BRL"

    assert invoice.supplier.name == "ABC Manufacturing Ltda."
    assert invoice.supplier.tax_id == "12345678000199"
    assert invoice.supplier.country_code == "BR"

    assert invoice.customer.name == "Customer Example"
    assert invoice.customer.tax_id == "12345678901"
    assert invoice.customer.country_code == "BR"

    assert invoice.lines == []
    assert invoice.totals is None
    assert invoice.source_format == InvoiceFormat.NFE


def test_nfe_parser_rejects_missing_invoice_number(tmp_path: Path):
    invalid_xml = VALID_NFE_XML.replace(
        "<nNF>12345</nNF>",
        "",
    )

    xml_file = tmp_path / "missing_number.xml"
    xml_file.write_text(invalid_xml, encoding="utf-8")

    with pytest.raises(NFeParsingError, match="Required NF-e field"):
        NFeParser().parse(xml_file)


def test_nfe_parser_rejects_invalid_xml(tmp_path: Path):
    xml_file = tmp_path / "invalid.xml"
    xml_file.write_text("<NFe><broken>", encoding="utf-8")

    with pytest.raises(NFeParsingError, match="Invalid XML"):
        NFeParser().parse(xml_file)


def test_nfe_parser_rejects_missing_file(tmp_path: Path):
    missing_file = tmp_path / "does_not_exist.xml"

    with pytest.raises(FileNotFoundError):
        NFeParser().parse(missing_file)