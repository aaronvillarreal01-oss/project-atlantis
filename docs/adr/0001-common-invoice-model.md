# ADR 0001: Use a Common Invoice Model

## Status

Accepted

## Context

Project Atlantis will process digital invoices from multiple countries and
standards, including Brazil NF-e, European UBL and Peppol, and potentially
Mexico CFDI.

These formats use different XML structures and field names but represent
similar business concepts, such as suppliers, customers, invoice lines,
taxes, and totals.

Passing country-specific XML structures throughout the application would
couple validation, reporting, and analytics to individual formats.

## Decision

Project Atlantis will convert every supported invoice format into a shared
Common Invoice Model.

Country-specific parsers will be responsible for translating source
documents into this model.

Downstream components, including validators, reports, APIs, and dashboards,
will operate primarily on the Common Invoice Model rather than directly on
source XML.

## Consequences

### Benefits

- Validation logic can be reused across countries.
- Reporting is independent of the original invoice format.
- New formats can be added by creating additional parsers.
- The architecture supports future APIs and ERP integrations.

### Trade-offs

- Some country-specific information may not fit naturally into the common
  model.
- The model may need extensions as new formats are introduced.
- Source references must be preserved where traceability is required.
