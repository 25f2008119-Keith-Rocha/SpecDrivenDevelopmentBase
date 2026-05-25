# Spec — Reports CSV export (v0.1)

## What

Allow users to export the currently visible reports data as a downloadable CSV file from the reports page.

## Acceptance criteria

- WHEN the user clicks the CSV export button THE SYSTEM SHALL download a CSV file containing the currently visible report rows.
- WHEN the export is triggered THE SYSTEM SHALL include the report table headers as the first row in the CSV file.
- WHEN filtered report data is displayed THE SYSTEM SHALL export only the filtered rows currently shown on the reports page.
- WHEN no reports are available THE SYSTEM SHALL generate a CSV file containing only the headers.
- WHEN the CSV export succeeds THE SYSTEM SHALL return HTTP status code 200.
- WHEN an internal export error occurs THE SYSTEM SHALL return HTTP status code 500 with an error message.

## Out of scope

- Exporting reports in Excel or PDF format.
- Scheduling or automating report exports.
- Sending exported CSV files through email.

## Tests required

- `tests/test_csv_export.py`
  - `test_csv_export_returns_200`
  - `test_csv_export_contains_headers`
  - `test_csv_export_exports_filtered_rows_only`
  - `test_csv_export_empty_results`
  - `test_csv_export_content_type`

## Notes

Use FastAPI `StreamingResponse` for CSV downloads and ensure the response content type is `text/csv`.