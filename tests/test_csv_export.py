"""Tests for CSV export functionality."""

import csv
from io import StringIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_csv_export_returns_200():
    """WHEN export is triggered THEN status code should be 200."""
    response = client.get("/reports/export")
    assert response.status_code == 200


def test_csv_export_contains_headers():
    """WHEN export is triggered THEN CSV should include headers as first row."""
    response = client.get("/reports/export")
    csv_content = response.text
    lines = csv_content.strip().split("\n")

    assert len(lines) > 0
    headers = [h.strip() for h in lines[0].split(",")]
    expected_headers = ["id", "title", "status", "owner", "amount", "created_at"]
    assert headers == expected_headers


def test_csv_export_exports_filtered_rows_only():
    """WHEN filtered data is displayed THEN export should include only filtered rows."""
    response = client.get("/reports/export?status=approved")
    csv_content = response.text
    reader = csv.DictReader(StringIO(csv_content))
    rows = list(reader)

    for row in rows:
        assert row["status"] == "approved"


def test_csv_export_empty_results():
    """WHEN no reports match filters THEN CSV should contain only headers."""
    response = client.get("/reports/export?status=archived")
    csv_content = response.text
    lines = csv_content.strip().split("\n")

    assert len(lines) >= 1
    headers = [h.strip() for h in lines[0].split(",")]
    expected_headers = ["id", "title", "status", "owner", "amount", "created_at"]
    assert headers == expected_headers


def test_csv_export_content_type():
    """WHEN export is triggered THEN response content type should be text/csv."""
    response = client.get("/reports/export")
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
