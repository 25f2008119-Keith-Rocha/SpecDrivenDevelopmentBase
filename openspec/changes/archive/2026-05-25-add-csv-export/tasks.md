# Tasks: Add CSV export for reports

- [x] Add a new `format` query parameter to `/reports` in `app.main`.
  - Accept only `json` or `csv`
  - Default to `json`
  - Return 400 for invalid values

- [x] Keep the existing JSON response path intact.
  - Use the existing `ReportListResponse` model for `format=json`
  - Preserve current pagination, filtering, and sorting behavior

- [x] Implement RFC 4180 CSV serialization for `format=csv`.
  - Use Python's standard `csv` module
  - Serialize only public fields: `id`, `title`, `status`, `owner`, `amount`, `created_at`
  - Use `\r\n` line endings and proper quoting
  - Return `text/csv` as the response media type

- [x] Add tests for CSV export in a new test file.
  - Verify `GET /reports?format=csv` returns status 200 and `Content-Type: text/csv`
  - Verify CSV contains the expected header row and public report values
  - Verify `internal_id` and `owner_email` are not present in the CSV output
  - Verify invalid `format` values return HTTP 400
  - Verify filters and sorting are honored in CSV output

- [x] Add the change-specific delta spec file under `openspec/changes/add-csv-export/specs/reports/spec.md`.

- [x] Ensure the proposal and artifacts are complete and ready for implementation.
