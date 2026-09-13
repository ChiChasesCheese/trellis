"""A small thread-safe TTL (time-to-live) cache: `set(key, value)` remembers a value for a fixed
number of seconds, after which `get(key)` treats it as missing again. `ConfigManager` (see
manager.py) uses one instance of this to avoid re-resolving the same config key across every one
of its four layers on every single `get()` call.

Every method that touches `self._store` takes `self._lock` first -- plain dicts are not safe to
read and write from multiple threads at once, so all access to `_store` is expected to go through
this class rather than reaching into it directly.
"""

from __future__ import annotations

import threading
import time


class TTLCache:
    def __init__(self, ttl_seconds: float):
        self._ttl = ttl_seconds
        self._store: dict = {}  # key -> (value, expires_at_monotonic)
        self._lock = threading.Lock()

    def get(self, key):
        """Return the cached value for `key`, or `None` if it was never set or has expired."""
        with self._lock:
            entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at <= time.monotonic():
            return None
        return value

    def set(self, key, value) -> None:
        """Store `value` for `key`, resetting its TTL clock to `now + ttl_seconds`."""
        with self._lock:
            self._store[key] = (value, time.monotonic() + self._ttl)

    def invalidate(self, key) -> None:
        """Drop `key` from the cache, if present. A no-op if it isn't cached."""
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        """Drop every cached entry at once -- used when the values a key would resolve to may
        all have changed underneath the cache (e.g. a config source was reloaded)."""
        with self._lock:
            self._store.clear()

    def get_or_compute(self, key, factory):
        """Return the cached value for `key`; on a miss, call `factory()` (no arguments) to
        produce it, store the result, and return it. `factory` is only meant to run once per
        miss -- callers rely on it not being re-run just because two threads both saw a miss at
        the same time.
        """
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.set(key, value)
        return value
