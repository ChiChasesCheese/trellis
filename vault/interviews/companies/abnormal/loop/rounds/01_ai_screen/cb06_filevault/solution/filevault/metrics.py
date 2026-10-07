"""Process-wide counters. ``incr`` from anywhere; ``snapshot`` to read them all."""
from __future__ import annotations

import threading

_lock = threading.Lock()
_counters: dict[str, int] = {}


def incr(name: str, amount: int = 1) -> None:
    with _lock:
        _counters[name] = _counters.get(name, 0) + amount


def get(name: str) -> int:
    with _lock:
        return _counters.get(name, 0)


def snapshot() -> dict[str, int]:
    with _lock:
        return dict(sorted(_counters.items()))


def reset() -> None:
    """For tests."""
    with _lock:
        _counters.clear()
