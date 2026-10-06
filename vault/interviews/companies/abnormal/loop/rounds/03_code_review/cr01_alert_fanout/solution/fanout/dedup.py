"""Suppress duplicate notifications within a TTL window.

`claim` is an atomic check-and-set: the first caller for a key wins; `release` gives the claim back
when the delivery failed so a retry can try again.
"""
from __future__ import annotations

import threading
import time
from typing import Callable


class DedupCache:
    def __init__(self, ttl_s: int = 3600, clock: Callable[[], float] = time.time):
        self.ttl_s = ttl_s
        self._clock = clock
        self._lock = threading.Lock()
        self._claims: dict[str, float] = {}

    def claim(self, key: str) -> bool:
        with self._lock:
            now = self._clock()
            if len(self._claims) > 10_000:
                self._claims = {k: exp for k, exp in self._claims.items() if exp > now}
            exp = self._claims.get(key)
            if exp is not None and exp > now:
                return False
            self._claims[key] = now + self.ttl_s
            return True

    def release(self, key: str) -> None:
        with self._lock:
            self._claims.pop(key, None)
