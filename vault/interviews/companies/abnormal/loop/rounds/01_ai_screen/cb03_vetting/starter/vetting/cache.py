"""A tiny TTL cache for external lookups (carrier, IP intel, domain age)."""
from __future__ import annotations

import time
from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class TTLCache(Generic[T]):
    def __init__(self, ttl_seconds: float, clock: Callable[[], float] = time.monotonic) -> None:
        self.ttl = ttl_seconds
        self._clock = clock
        self._items: dict[str, tuple[float, T]] = {}

    def get_or_load(self, key: str, loader: Callable[[str], T]) -> T:
        now = self._clock()
        hit = self._items.get(key)
        if hit is not None and now - hit[0] < self.ttl:
            return hit[1]
        value = loader(key)
        self._items[key] = (now, value)
        return value

    def __len__(self) -> int:
        return len(self._items)
