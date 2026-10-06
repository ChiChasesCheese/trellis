"""Process-wide counters. Cheap and in-memory; the CLI prints them after an ingest."""
from __future__ import annotations

from collections import Counter
from threading import Lock


class Metrics:
    def __init__(self) -> None:
        self._counts: Counter[str] = Counter()
        self._lock = Lock()

    def incr(self, name: str, n: int = 1) -> None:
        with self._lock:
            self._counts[name] += n

    def get(self, name: str) -> int:
        return self._counts.get(name, 0)

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(sorted(self._counts.items()))

    def reset(self) -> None:
        with self._lock:
            self._counts.clear()


metrics = Metrics()
