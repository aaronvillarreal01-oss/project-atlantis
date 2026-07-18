from pathlib import Path
import xml.etree.ElementTree as ET

from project_atlantis.intake.detection_models import InvoiceDetectionResult
from project_atlantis.intake.registry import find_format


class UnsupportedInvoiceFormatError(ValueError):
    """Raised when Atlantis cannot identify the invoice format."""


def split_xml_tag(tag: str) -> tuple[str, str]:
    """Return the namespace and local name from an XML tag."""
    if tag.startswith("{") and "}" in tag:
        namespace, local_name = tag[1:].split("}", 1)
        return namespace, local_name

    return "", tag


def detect_invoice(file_path: str | Path) -> InvoiceDetectionResult:
    """Detect the invoice format from an XML file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Invoice file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Invoice path is not a file: {path}")

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML invoice: {path}") from exc

    namespace, root_element = split_xml_tag(root.tag)

    format_definition = find_format(
        root_element=root_element,
        namespace=namespace,
    )

    if format_definition is None:
        raise UnsupportedInvoiceFormatError(
            "Unsupported invoice format: "
            f"root_element={root_element!r}, namespace={namespace!r}"
        )

    version = (
        root.attrib.get("versao")
        or root.attrib.get("version")
        or root.attrib.get("Version")
    )

    return InvoiceDetectionResult(
        invoice_format=format_definition.invoice_format,
        root_element=root_element,
        namespace=namespace,
        version=version,
        country_code=format_definition.country_code,
        authority_system=format_definition.authority_system,
    )