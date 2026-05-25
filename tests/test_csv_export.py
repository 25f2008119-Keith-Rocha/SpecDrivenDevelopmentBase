"""Tests for CSV export support on the Reports API."""

from __future__ import annotations

import csv
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reports_csv_export_returns_text_csv() -> None:
    r = client.get("/reports", params={"format": "csv", "limit": 5})

    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")

    rows = list(csv.reader(r.text.splitlines()))
    assert rows[0] == ["id", "title", "status", "owner", "amount", "created_at"]
    assert len(rows) == 6


def test_reports_csv_export_omits_internal_fields() -> None:
    r = client.get("/reports", params={"format": "csv", "limit": 10})

    assert r.status_code == 200
    assert "internal_id" not in r.text
    assert "owner_email" not in r.text


def test_reports_csv_export_honors_filters_and_sorting() -> None:
    r = client.get(
        "/reports",
        params={
            "format": "csv",
            "status": "approved",
            "sort": "amount",
            "descending": "false",
            "limit": 10,
        },
    )

    assert r.status_code == 200

    rows = list(csv.reader(r.text.splitlines()))
    assert rows[0] == ["id", "title", "status", "owner", "amount", "created_at"]
    data_rows = rows[1:]
    assert data_rows
    assert all(row[2] == "approved" for row in data_rows)

    amounts = [float(row[4]) for row in data_rows]
    assert amounts == sorted(amounts)


def test_reports_csv_export_invalid_format_returns_400() -> None:
    r = client.get("/reports", params={"format": "xml"})

    assert r.status_code == 400
