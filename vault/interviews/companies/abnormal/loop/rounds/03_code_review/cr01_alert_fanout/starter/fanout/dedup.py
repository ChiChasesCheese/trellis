"""Suppress duplicate notifications for the same alert within a TTL window."""
from __future__ import annotations

import time
from typing import Callable


class DedupCache:
    def __init__(self, ttl_s: int = 3600, clock: Callable[[], float] = time.time):
        self.ttl_s = ttl_s
        self._clock = clock
        self._seen: dict[str, float] = {}

    def seen(self, key: str) -> bool:
        expires = self._seen.get(key)
        return expires is not None and expires > self._clock()

    def add(self, key: str) -> None:
        now = self._clock()
        for k, exp in list(self._seen.items()):  # drop expired entries
            if exp <= now:
                del self._seen[k]
        self._seen[key] = now + self.ttl_s
