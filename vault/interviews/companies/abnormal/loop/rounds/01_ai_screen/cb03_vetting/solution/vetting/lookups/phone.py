from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from vetting.cache import TTLCache


class LineType(StrEnum):
    MOBILE = "MOBILE"
    LANDLINE = "LANDLINE"
    VOIP = "VOIP"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class PhoneInfo:
    line_type: LineType
    carrier: str | None = None
    country: str | None = None


class PhoneLookup:
    """Carrier lookup keyed by E.164 number."""

    def __init__(self, table: dict[str, dict], cache: TTLCache[PhoneInfo]) -> None:
        self._table = table
        self._cache = cache

    @classmethod
    def from_file(cls, path: Path, cache: TTLCache[PhoneInfo]) -> "PhoneLookup":
        return cls(json.loads(path.read_text()), cache)

    def lookup(self, e164: str) -> PhoneInfo:
        return self._cache.get_or_load(e164, self._load)

    def _load(self, e164: str) -> PhoneInfo:
        row = self._table.get(e164)
        if row is None:
            return PhoneInfo(LineType.UNKNOWN)
        return PhoneInfo(LineType(row["line_type"]), row.get("carrier"), row.get("country"))
