"""Tiny statistics helpers (stdlib `statistics` is overkill for population stats on short lists)."""
from __future__ import annotations

from math import sqrt
from typing import Sequence


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def pstdev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    return sqrt(sum((v - mu) ** 2 for v in values) / len(values))


def percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolated percentile, q in [0, 1]."""
    if not values:
        return 0.0
    ordered = sorted(values)
    pos = q * (len(ordered) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)
