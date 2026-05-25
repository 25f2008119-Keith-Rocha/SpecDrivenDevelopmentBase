"""Reports query layer.

Pure functions that filter, sort, and paginate the in-memory dataset. Kept separate
from the HTTP layer (`main.py`) so it can be reused by any future export feature.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable
import csv
import io

from app.data import all_reports
from app.models import Report, ReportPublic, ReportStatus


_SORTABLE_FIELDS = {"id", "title", "status", "owner", "amount", "created_at"}


def render_reports_csv(rows: Iterable[Report]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(["id", "title", "status", "owner", "amount", "created_at"])
    for report in rows:
        public = ReportPublic.from_internal(report)
        writer.writerow([
            public.id,
            public.title,
            public.status,
            public.owner,
            public.amount,
            public.created_at.isoformat(),
        ])
    return buffer.getvalue()


def query(
    *,
    status: ReportStatus | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort: str = "created_at",
    descending: bool = True,
) -> list[Report]:
    """Filter and sort reports. Pagination is applied by the caller."""

    if sort not in _SORTABLE_FIELDS:
        raise ValueError(f"Unsupported sort field: {sort!r}")

    rows: Iterable[Report] = all_reports()

    if status is not None:
        rows = (r for r in rows if r.status == status)
    if date_from is not None:
        rows = (r for r in rows if r.created_at >= date_from)
    if date_to is not None:
        rows = (r for r in rows if r.created_at <= date_to)

    return sorted(rows, key=lambda r: getattr(r, sort), reverse=descending)
