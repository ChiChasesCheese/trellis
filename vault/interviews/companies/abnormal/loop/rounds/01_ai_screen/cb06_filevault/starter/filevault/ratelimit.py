"""A token bucket. Thread-safe; the clock is injectable so tests never sleep."""
from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable


class TokenBucket:
    """Holds up to ``capacity`` tokens and refills ``rate`` tokens per second."""

    def __init__(self, rate: float, capacity: float, clock: Callable[[], float] = time.monotonic):
        if rate <= 0 or capacity <= 0:
            raise ValueError("rate and capacity must be positive")
        self.rate = rate
        self.capacity = capacity
        self._clock = clock
        self._tokens = float(capacity)
        self._updated = clock()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = self._clock()
        elapsed = max(0.0, now - self._updated)
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._updated = now

    def try_take(self, tokens: float = 1.0) -> bool:
        """Take ``tokens`` if available. Never blocks."""
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def seconds_until(self, tokens: float = 1.0) -> int:
        """Whole seconds (rounded up, at least 1) until ``tokens`` could be taken."""
        with self._lock:
            self._refill()
            missing = max(0.0, tokens - self._tokens)
            return max(1, math.ceil(missing / self.rate))
