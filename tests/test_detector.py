from pathlib import Path

import pytest

from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.intake.detector import (
    UnsupportedInvoiceFormatError,
    detect_invoice,
)


TEST_DATA = Path(__file__).parent / "data"


def test_detect_nfe_invoice():
    result = detect_invoice(TEST_DATA / "nfe_sample.xml")

    assert result.invoice_format == InvoiceFormat.NFE
    assert result.country_code == "BR"
    assert result.authority_system == "SEFAZ"
    assert result.version == "4.00"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        detect_invoice(TEST_DATA / "does_not_exist.xml")


def test_invalid_xml(tmp_path):
    xml_file = tmp_path / "invalid.xml"
    xml_file.write_text("<NFe><invalid>", encoding="utf-8")

    with pytest.raises(ValueError):
        detect_invoice(xml_file)


def test_unknown_invoice_format(tmp_path):
    xml_file = tmp_path / "unknown.xml"

    xml_file.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<UnknownInvoice xmlns="https://example.com/invoice"/>
""",
        encoding="utf-8",
    )

    with pytest.raises(UnsupportedInvoiceFormatError):
        detect_invoice(xml_file)