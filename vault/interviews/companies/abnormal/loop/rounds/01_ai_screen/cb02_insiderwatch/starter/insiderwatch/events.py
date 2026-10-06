"""The normalized event model. Every connector produces these; nothing downstream sees raw records."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Any, Iterable


class Action(str, Enum):
    LOGIN = "LOGIN"
    LOGIN_FAILED = "LOGIN_FAILED"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_DELETE = "FILE_DELETE"
    FILE_SHARE_EXTERNAL = "FILE_SHARE_EXTERNAL"
    EMAIL_FORWARD_EXTERNAL = "EMAIL_FORWARD_EXTERNAL"
    MESSAGE_EXPORT = "MESSAGE_EXPORT"


def normalize_user(value: str) -> str:
    """Users are keyed by lower-cased, stripped email address everywhere."""
    return value.strip().lower()


def email_domain(address: str) -> str:
    return address.rsplit("@", 1)[-1].strip().lower() if "@" in address else ""


def is_external(address: str, internal_domains: Iterable[str]) -> bool:
    """True when `address` has a domain that is not one of the tenant's own."""
    domain = email_domain(address)
    return bool(domain) and domain not in {d.lower() for d in internal_domains}


@dataclass(frozen=True)
class Event:
    user: str
    ts: datetime  # always timezone-aware UTC
    action: Action
    bytes: int = 0
    target: str = ""
    source: str = ""
    attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.ts.tzinfo is None:
            raise ValueError("Event.ts must be timezone-aware")
        object.__setattr__(self, "user", normalize_user(self.user))
        object.__setattr__(self, "ts", self.ts.astimezone(timezone.utc))

    @property
    def day(self) -> date:
        return self.ts.date()

    def sort_key(self) -> tuple[datetime, str, str]:
        return (self.ts, self.source, self.user)


def day_start(day: date) -> datetime:
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)


def day_end(day: date) -> datetime:
    """Last instant of `day` (UTC), inclusive upper bound for replay."""
    return day_start(day) + timedelta(days=1) - timedelta(microseconds=1)
