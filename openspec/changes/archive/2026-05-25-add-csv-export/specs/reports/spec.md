# Changes to Reports spec: Add CSV export

## ADDED Requirements

### Requirement: CSV export for `/reports`
THE system SHALL support CSV export from `GET /reports` using a `format` query parameter.

#### Scenario: CSV export returns `text/csv`
- **WHEN** the user calls `GET /reports?format=csv`
- **THEN** the response SHALL have `Content-Type: text/csv`
- **AND** the response body SHALL be valid RFC 4180 CSV
- **AND** the CSV SHALL include a header row with `id,title,status,owner,amount,created_at`

#### Scenario: CSV export omits internal fields
- **WHEN** the user requests `GET /reports?format=csv`
- **THEN** the CSV output SHALL NOT contain `internal_id`
- **AND** the CSV output SHALL NOT contain `owner_email`

#### Scenario: CSV export honors filters and sorting
- **WHEN** the user calls `GET /reports?format=csv&status=approved&sort=amount&descending=false`
- **THEN** every row in the CSV SHALL have `status` equal to `approved`
- **AND** the rows SHALL be ordered by `amount` ascending

#### Scenario: invalid format value returns 400
- **WHEN** the user calls `GET /reports?format=xml`
- **THEN** the response SHALL be HTTP 400

## Specification notes
- CSV export MUST use the standard-library `csv` module for serialization.
- CSV output MUST follow RFC 4180 formatting.
