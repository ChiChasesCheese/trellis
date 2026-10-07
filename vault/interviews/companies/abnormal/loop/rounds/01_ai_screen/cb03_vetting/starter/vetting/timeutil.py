"""Timestamp helpers. Everything stored or returned by this package is timezone-aware UTC."""
from __future__ import annotations

from datetime import datetime, timezone

UTC = timezone.utc


def parse_ts(value: str) -> datetime:
    """Parse an ISO-8601 timestamp (``Z`` or any offset, optional fractional seconds) to UTC.

    Naive timestamps are rejected: a source that omits the offset is a bad record, not a guess.
    """
    parsed = datetime.fromisoformat(value.strip())
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp has no UTC offset: {value!r}")
    return parsed.astimezone(UTC)


def to_iso(moment: datetime) -> str:
    """Canonical string form used in the database and the API, e.g. ``2026-09-14T17:22:00+00:00``."""
    return moment.astimezone(UTC).isoformat(timespec="seconds")


def utcnow() -> datetime:
    return datetime.now(UTC)
