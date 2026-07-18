from dataclasses import dataclass

from project_atlantis.core.enums import InvoiceFormat


@dataclass(frozen=True)
class FormatDefinition:
    """Defines the identifying characteristics of an invoice format."""

    invoice_format: InvoiceFormat
    root_elements: tuple[str, ...]
    namespaces: tuple[str, ...]
    country_code: str | None = None
    authority_system: str | None = None


FORMAT_REGISTRY: tuple[FormatDefinition, ...] = (
    FormatDefinition(
        invoice_format=InvoiceFormat.NFE,
        root_elements=("NFe", "nfeProc"),
        namespaces=("http://www.portalfiscal.inf.br/nfe",),
        country_code="BR",
        authority_system="SEFAZ",
    ),
    FormatDefinition(
        invoice_format=InvoiceFormat.UBL,
        root_elements=("Invoice",),
        namespaces=(
            "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        ),
        country_code=None,
        authority_system="UBL",
    ),
    FormatDefinition(
        invoice_format=InvoiceFormat.CFDI,
        root_elements=("Comprobante",),
        namespaces=(
            "http://www.sat.gob.mx/cfd/4",
        ),
        country_code="MX",
        authority_system="SAT",
    ),
)


def find_format(
    root_element: str,
    namespace: str,
) -> FormatDefinition | None:
    """
    Find a registered invoice format using both root element and namespace.

    Returns None when no registered format matches.
    """

    for definition in FORMAT_REGISTRY:
        root_matches = root_element in definition.root_elements
        namespace_matches = namespace in definition.namespaces

        if root_matches and namespace_matches:
            return definition

    return None