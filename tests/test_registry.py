from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.intake.registry import find_format


def test_find_nfe_format():
    result = find_format(
        root_element="NFe",
        namespace="http://www.portalfiscal.inf.br/nfe",
    )

    assert result is not None
    assert result.invoice_format == InvoiceFormat.NFE
    assert result.country_code == "BR"
    assert result.authority_system == "SEFAZ"


def test_find_processed_nfe_format():
    result = find_format(
        root_element="nfeProc",
        namespace="http://www.portalfiscal.inf.br/nfe",
    )

    assert result is not None
    assert result.invoice_format == InvoiceFormat.NFE


def test_unknown_format_returns_none():
    result = find_format(
        root_element="UnknownInvoice",
        namespace="https://example.com/unknown",
    )

    assert result is None