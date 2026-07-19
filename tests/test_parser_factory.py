import pytest

from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.intake.detection_models import InvoiceDetectionResult
from project_atlantis.parsers import UnsupportedParserError, get_parser
from project_atlantis.parsers.nfe import NFeParser


def test_factory_returns_nfe_parser():
    detection = InvoiceDetectionResult(
        invoice_format=InvoiceFormat.NFE,
        root_element="NFe",
        namespace="http://www.portalfiscal.inf.br/nfe",
        version="4.00",
        country_code="BR",
        authority_system="SEFAZ",
    )

    parser = get_parser(detection)

    assert isinstance(parser, NFeParser)


def test_factory_rejects_unsupported_format():
    detection = InvoiceDetectionResult(
        invoice_format=InvoiceFormat.UNKNOWN,
        root_element="UnknownInvoice",
        namespace="https://example.com/unknown",
    )

    with pytest.raises(UnsupportedParserError):
        get_parser(detection)