# Design: CSV export for /reports

## Route behavior
Extend the existing `GET /reports` route with a new query parameter:
- `format: str = Query("json", description="Response format", pattern="^(json|csv)$")`

When `format=csv`:
- use the existing `app.reports.query()` helper to get the filtered, sorted report rows
- apply pagination through `offset` and `limit` as the endpoint already does
- serialize the result rows into CSV using the standard library `csv` module
- return a raw CSV body with `Content-Type: text/csv`

When `format=json`:
- preserve the current JSON response model `ReportListResponse`
- keep the existing error handling for invalid sort fields

## CSV serialization
Use only public fields from `ReportPublic.from_internal()`:
- `id`
- `title`
- `status`
- `owner`
- `amount`
- `created_at`

CSV rendering details:
- use `csv.writer` with `lineterminator="\r\n"` for RFC 4180 compatibility
- quote fields as needed via `csv.QUOTE_MINIMAL`
- convert `created_at` to ISO 8601 strings in the CSV output

## Implementation approach
1. Add `format` query parameter to `app.main.list_reports`
2. Keep the existing JSON path unchanged for backward compatibility
3. Add a helper in `app.reports` or `app.main` to serialize a sequence of `ReportPublic` objects into RFC 4180 CSV
4. Use FastAPI's `Response` class with `media_type="text/csv"` when `format=csv`
5. Add tests covering CSV export semantics and invalid `format` handling

## Data and safety
- Use `ReportPublic.from_internal()` to ensure internal-only fields are never leaked
- Keep the report query layer reusable and independent of output format
- Preserve `offset`/`limit` behavior so existing pagination controls remain valid for CSV export
