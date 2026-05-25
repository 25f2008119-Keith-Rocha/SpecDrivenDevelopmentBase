# Proposal: Add CSV export for reports

## What
Add CSV export support to the existing `GET /reports` capability.

The API will accept a new query parameter, `format`, with values `json` (default) or `csv`.
When `format=csv`, the endpoint will return the same filtered and sorted report rows as RFC 4180 CSV with media type `text/csv`.

## Why
Currently the Reports API only exposes JSON output. Many integration and reporting use cases require a simple CSV export of the same filtered report dataset.

This change keeps the existing JSON behavior intact while adding a user-facing export format that:
- reuses the same `status`, `date_from`, `date_to`, `sort`, `descending`, `offset`, and `limit` semantics
- never exposes internal-only fields (`internal_id`, `owner_email`)
- produces RFC 4180-compliant CSV using Python's standard-library `csv` module

## Acceptance criteria
- `GET /reports?format=csv` returns `Content-Type: text/csv`
- The CSV body includes a header row and one row per returned report
- CSV output contains only public fields: `id`, `title`, `status`, `owner`, `amount`, `created_at`
- Filters and sort behave the same as JSON output
- Invalid `format` values return HTTP 400
- Internal-only fields are never included in CSV output

## Non-goals
- Adding Excel/XLSX, PDF, or any export format other than CSV
- Changing the existing `/reports` JSON response contract
- Adding a separate `/reports/export` endpoint
