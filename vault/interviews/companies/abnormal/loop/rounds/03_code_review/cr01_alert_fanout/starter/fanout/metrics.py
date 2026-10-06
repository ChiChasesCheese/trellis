"""Process-local counters; the real exporter scrapes `snapshot()`."""
from __future__ import annotations

import threading
from collections import Counter

_lock = threading.Lock()
_counts: Counter[str] = Counter()


def inc(name: str, n: int = 1) -> None:
    with _lock:
        _counts[name] += n


def snapshot() -> dict[str, int]:
    with _lock:
        return dict(_counts)


def reset() -> None:
    with _lock:
        _counts.clear()
