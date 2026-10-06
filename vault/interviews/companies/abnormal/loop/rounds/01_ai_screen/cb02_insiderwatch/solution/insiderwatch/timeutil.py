"""Time helpers. All storage is UTC; local time only matters for business-hours checks."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Iterator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .errors import InsiderWatchError


def parse_ts(value: str | int | float) -> datetime:
    """Parse an API timestamp to an aware UTC datetime.

    Accepts epoch seconds, `...Z`, explicit offsets, and naive ISO strings (assumed UTC,
    which is how the M365 audit log writes CreationTime).
    """
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InsiderWatchError(f"bad date {value!r}, expected YYYY-MM-DD") from exc


def zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise InsiderWatchError(f"unknown timezone {name!r}") from exc


def to_local(ts: datetime, tz_name: str) -> datetime:
    return ts.astimezone(zone(tz_name))


def is_business_hours(ts: datetime, tz_name: str, start_hour: int = 9, end_hour: int = 17) -> bool:
    """Mon-Fri, [start_hour, end_hour) in the user's local time."""
    local = to_local(ts, tz_name)
    return local.weekday() < 5 and start_hour <= local.hour < end_hour


def daterange(start: date, end: date) -> Iterator[date]:
    """Days from `start` up to but excluding `end`."""
    current = start
    while current < end:
        yield current
        current += timedelta(days=1)
