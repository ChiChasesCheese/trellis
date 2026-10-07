"""Sender-domain reputation, backed by ``fixtures/intel/senders.json``."""
from __future__ import annotations

import json
from pathlib import Path


class SenderIntel:
    def __init__(self, path: Path):
        self._scores: dict[str, int] = json.loads(Path(path).read_text())["domains"]

    def score(self, domain: str) -> int | None:
        """Risk 0-100 for a sender domain, or ``None`` when we have no intel on it."""
        return self._scores.get(domain.lower())
