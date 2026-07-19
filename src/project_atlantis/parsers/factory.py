from project_atlantis.core.enums import InvoiceFormat
from project_atlantis.intake.detection_models import InvoiceDetectionResult
from project_atlantis.parsers.base import BaseParser
from project_atlantis.parsers.nfe import NFeParser


class UnsupportedParserError(ValueError):
    """Raised when no parser is available for a detected format."""


def get_parser(detection: InvoiceDetectionResult) -> BaseParser:
    """Return the correct parser for a detected invoice format."""

    if detection.invoice_format == InvoiceFormat.NFE:
        return NFeParser()

    raise UnsupportedParserError(
        f"No parser available for format: {detection.invoice_format.value}"
    )