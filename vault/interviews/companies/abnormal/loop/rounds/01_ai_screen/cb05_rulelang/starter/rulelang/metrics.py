"""Process-wide counters. Deliberately tiny: a dict behind a lock.

Usage: ``metrics.incr("loader.bad_record", reason="bad_ts")``.
"""
from __future__ import annotations

import threading
from collections import Counter

_lock = threading.Lock()
_counters: Counter[str] = Counter()


def _key(name: str, labels: dict[str, str]) -> str:
    if not labels:
        return name
    inner = ",".join(f"{k}={labels[k]}" for k in sorted(labels))
    return f"{name}{{{inner}}}"


def incr(name: str, n: int = 1, **labels: str) -> None:
    with _lock:
        _counters[_key(name, labels)] += n


def get(name: str, **labels: str) -> int:
    with _lock:
        return _counters[_key(name, labels)]


def total(name: str) -> int:
    """Sum of a counter across every label combination."""
    with _lock:
        return sum(v for k, v in _counters.items() if k == name or k.startswith(name + "{"))


def snapshot() -> dict[str, int]:
    with _lock:
        return dict(sorted(_counters.items()))


def reset() -> None:
    with _lock:
        _counters.clear()
