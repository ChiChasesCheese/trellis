"""In-memory stand-in for Redis: bytes values with a TTL. Swap for a redis client in production."""
from __future__ import annotations

import threading
import time
from typing import Callable, Optional


class Cache:
    def __init__(self, clock: Callable[[], float] = time.monotonic):
        self._clock = clock
        self._lock = threading.Lock()
        self._data: dict[str, tuple[bytes, float]] = {}

    def get(self, key: str) -> Optional[bytes]:
        with self._lock:
            hit = self._data.get(key)
            if hit is None:
                return None
            value, expires = hit
            if expires <= self._clock():
                del self._data[key]
                return None
            return value

    def set(self, key: str, value: bytes, ttl: float) -> None:
        with self._lock:
            self._data[key] = (value, self._clock() + ttl)

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)

    def keys(self, prefix: str = "") -> list[str]:
        with self._lock:
            return [k for k in self._data if k.startswith(prefix)]
