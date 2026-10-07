"""UTC helpers. Everything stored or compared in rulelang is a timezone-aware UTC datetime."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

UTC = timezone.utc


def utcnow() -> datetime:
    return datetime.now(UTC)


def parse_ts(value: str | datetime) -> datetime:
    """Parse an ISO-8601 timestamp (``Z`` or an offset) into aware UTC; naive input is taken as UTC."""
    if isinstance(value, datetime):
        dt = value
    else:
        text = value.strip()
        if text.endswith(("Z", "z")):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def iso(dt: datetime) -> str:
    """Canonical storage form; fixed width so string comparison matches time order."""
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def window_start(now: datetime, minutes: float) -> datetime:
    return now - timedelta(minutes=minutes)
