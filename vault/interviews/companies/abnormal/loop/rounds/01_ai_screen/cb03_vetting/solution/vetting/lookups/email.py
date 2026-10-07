from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from vetting.cache import TTLCache


@dataclass(frozen=True)
class EmailInfo:
    domain: str
    disposable: bool = False
    domain_age_days: int | None = None


class EmailLookup:
    """Domain reputation keyed by (already normalized) domain."""

    def __init__(self, data: dict, cache: TTLCache[EmailInfo]) -> None:
        self._disposable = set(data.get("disposable_domains", []))
        self._ages: dict[str, int] = data.get("domain_age_days", {})
        self._cache = cache

    @classmethod
    def from_file(cls, path: Path, cache: TTLCache[EmailInfo]) -> "EmailLookup":
        return cls(json.loads(path.read_text()), cache)

    def lookup(self, domain: str) -> EmailInfo:
        return self._cache.get_or_load(domain, self._load)

    def _load(self, domain: str) -> EmailInfo:
        return EmailInfo(domain, domain in self._disposable, self._ages.get(domain))
