"""URL reputation lookup. The interface is what analyzers depend on; the fixtures-backed class is
the stand-in for a real intel provider."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import urlsplit

from quarantine.errors import LookupUnavailable


@dataclass(frozen=True)
class UrlIntel:
    host: str
    category: str
    score: int  # 0 (clean or unknown) .. 100 (known phishing)


class UrlLookup(Protocol):
    def check(self, url: str) -> UrlIntel:
        """Raises ``LookupUnavailable`` when the provider cannot answer."""
        ...


class FixtureUrlLookup:
    """Reads ``fixtures/intel/urls.json``; ``unavailable`` hosts simulate a provider outage."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def check(self, url: str) -> UrlIntel:
        host = (urlsplit(url).hostname or "").lower()
        data = json.loads(self.path.read_text())
        if host in data.get("unavailable", []):
            raise LookupUnavailable(f"intel provider timed out for {host}")
        entry = data["hosts"].get(host)
        if entry is None:
            return UrlIntel(host, "unknown", 0)
        return UrlIntel(host, entry["category"], entry["score"])
