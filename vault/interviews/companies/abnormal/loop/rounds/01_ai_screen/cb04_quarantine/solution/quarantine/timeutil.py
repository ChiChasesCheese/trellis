"""Time helpers. Datetimes in this codebase are timezone-aware and compared in UTC."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """Convert an aware datetime to UTC. Naive datetimes are a bug, so they raise."""
    if dt.tzinfo is None:
        raise ValueError("naive datetime: attach a timezone first")
    return dt.astimezone(timezone.utc)


def iso(dt: datetime) -> str:
    """Canonical stored form: UTC, whole seconds, ``2026-09-15T16:30:00+00:00``."""
    return to_utc(dt).isoformat(timespec="seconds")


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def parse_rfc2822(value: str | None) -> datetime | None:
    """Parse an RFC 2822 ``Date`` header; ``None`` when absent or malformed.

    The returned datetime keeps the header's own UTC offset. A ``-0000`` offset (no zone
    information) is read as UTC.
    """
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)


def hours_before(dt: datetime, hours: float) -> datetime:
    return dt - timedelta(hours=hours)
