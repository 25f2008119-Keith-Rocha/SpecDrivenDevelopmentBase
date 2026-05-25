"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException, Query, Response

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query, render_reports_csv

app = FastAPI(title="SDD Workshop — Reports API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    format: str = Query("json", description="Response format"),
) -> ReportListResponse | Response:
    """Return a paginated list of reports.

    Public fields only — `internal_id` and `owner_email` are stripped via
    `ReportPublic.from_internal`.
    """

    if format not in {"json", "csv"}:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format!r}")

    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    page = rows[offset : offset + limit]

    if format == "csv":
        csv_body = render_reports_csv(page)
        return Response(content=csv_body, media_type="text/csv")

    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )
