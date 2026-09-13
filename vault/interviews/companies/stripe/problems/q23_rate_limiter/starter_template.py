"""q23 Rate Limiter — YOUR implementation. Run: python drill.py test q23

Part 1 SlidingWindow (global) -> Part 2 RateLimiter (per client) -> Part 3 weights
-> Part 4 TokenBucket with lazy refill + cleanup(now_ms, idle_ms).
"""
from __future__ import annotations

import sys
from collections import deque


class SlidingWindow:
    """Part 1: at most `limit` weight in the window (t - window_ms, t]."""

    def __init__(self, limit: int, window_ms: int) -> None:
        self.limit, self.window_ms = limit, window_ms
        self.events: deque = deque()  # (ts, weight) of ALLOWED requests
        # TODO

    def allow(self, ts_ms: int, weight: int = 1) -> bool:
        # TODO (raise ValueError('out-of-order timestamp') if ts_ms < last seen ts)
        return False


class RateLimiter:
    """Parts 2-3: one SlidingWindow per client key."""

    def __init__(self, limit: int, window_ms: int) -> None:
        self.limit, self.window_ms = limit, window_ms
        self.windows: dict[str, SlidingWindow] = {}

    def allow(self, client: str, ts_ms: int, weight: int = 1) -> bool:
        # TODO
        return False

    def cleanup(self, now_ms: int, idle_ms: int) -> int:
        """Evict clients with an empty window at now_ms whose last request is >= idle_ms old."""
        # TODO
        return 0


class TokenBucket:
    """Part 4: per-client bucket, starts full, lazy refill of refill_per_sec tokens/second."""

    def __init__(self, capacity: int, refill_per_sec: int) -> None:
        self.capacity, self.refill_per_sec = capacity, refill_per_sec
        self.buckets: dict[str, list] = {}  # client -> [milli_tokens, last_ts]

    def allow(self, client: str, ts_ms: int, cost: int = 1) -> bool:
        # TODO
        return False

    def cleanup(self, now_ms: int, idle_ms: int) -> int:
        # TODO
        return 0


def process(lines: list[str], part: int) -> list[str]:
    """Drive a limiter with the stdin lines (after the PART line); return ALLOW/DENY/ERROR/EVICTED n."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = process(lines[1:], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
