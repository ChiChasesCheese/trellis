"""Time helpers. Every timestamp inside Sentinel is a timezone-aware UTC datetime."""
from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta, timezone

UTC = timezone.utc


def utcnow() -> datetime:
    return datetime.now(UTC)


def parse_ts(value: str | int | float) -> datetime:
    """Parse an ISO-8601 string (with offset or Z) or epoch seconds into aware UTC."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(value, tz=UTC)
    if not isinstance(value, str):
        raise ValueError(f"unsupported timestamp: {value!r}")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError(f"timestamp has no timezone: {value!r}")
    return dt.astimezone(UTC)


def iso(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def sliding_window(timestamps: Sequence[datetime], window: timedelta) -> int:
    """Largest number of timestamps that fall inside any span of length ``window``.

    ``timestamps`` need not be sorted. A span is closed on both ends.
    """
    ordered = sorted(timestamps)
    best = 0
    start = 0
    for end, ts in enumerate(ordered):
        while ts - ordered[start] > window:
            start += 1
        best = max(best, end - start + 1)
    return best
