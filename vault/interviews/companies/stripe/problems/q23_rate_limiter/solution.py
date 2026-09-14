"""q23 Rate Limiter — reference solution.

Sliding window: a deque of (ts, weight) for ALLOWED requests only, plus a running sum, so each
request is O(1) amortised (each event is appended once and popped once).
Token bucket: integer milli-tokens (elapsed_ms * refill_per_sec == milli-tokens gained), no floats.
"""
from __future__ import annotations

import sys
from collections import deque


class SlidingWindow:
    """Part 1 (and the per-client building block of Parts 2-3)."""

    def __init__(self, limit: int, window_ms: int) -> None:
        self.limit, self.window_ms = limit, window_ms
        self.events: deque = deque()  # (ts, weight) of allowed requests, oldest first
        self.total = 0                # sum of weights currently in the deque
        self.last_ts = -1             # last SEEN timestamp (allowed or denied)

    def allow(self, ts_ms: int, weight: int = 1) -> bool:
        if weight <= 0:
            raise ValueError("weight must be positive")
        if ts_ms < self.last_ts:
            raise ValueError("out-of-order timestamp")
        self.last_ts = ts_ms
        # drop everything at or before ts - window: the window is (ts - window_ms, ts]
        cutoff = ts_ms - self.window_ms
        ev = self.events
        while ev and ev[0][0] <= cutoff:
            self.total -= ev.popleft()[1]
        if self.total + weight > self.limit:  # non-strict: sum + weight == limit still allowed
            return False
        ev.append((ts_ms, weight))
        self.total += weight
        return True


class RateLimiter:
    """Parts 2-3: independent SlidingWindow per client, created lazily."""

    def __init__(self, limit: int, window_ms: int) -> None:
        self.limit, self.window_ms = limit, window_ms
        self.windows: dict[str, SlidingWindow] = {}

    def allow(self, client: str, ts_ms: int, weight: int = 1) -> bool:
        w = self.windows.get(client)
        if w is None:
            w = self.windows[client] = SlidingWindow(self.limit, self.window_ms)
        return w.allow(ts_ms, weight)

    def cleanup(self, now_ms: int, idle_ms: int) -> int:
        """Evict clients idle for >= idle_ms whose window (now - window_ms, now] holds nothing."""
        idle = [
            c for c, w in self.windows.items()
            if w.last_ts <= now_ms - idle_ms and (not w.events or w.events[-1][0] <= now_ms - self.window_ms)
        ]
        for c in idle:
            del self.windows[c]
        return len(idle)


class TokenBucket:
    """Part 4: bucket per client, starts full; lazy refill in exact milli-tokens."""

    def __init__(self, capacity: int, refill_per_sec: int) -> None:
        self.capacity, self.refill_per_sec = capacity, refill_per_sec
        self.buckets: dict[str, list] = {}  # client -> [milli_tokens, last_ts]

    def allow(self, client: str, ts_ms: int, cost: int = 1) -> bool:
        if cost <= 0:
            raise ValueError("cost must be positive")
        b = self.buckets.get(client)
        if b is None:
            b = self.buckets[client] = [self.capacity * 1000, ts_ms]  # new client: full bucket
        elif ts_ms < b[1]:
            raise ValueError("out-of-order timestamp")
        # elapsed_ms * refill_per_sec tokens/s == elapsed_ms * refill_per_sec milli-tokens; cap at capacity
        b[0] = min(self.capacity * 1000, b[0] + (ts_ms - b[1]) * self.refill_per_sec)
        b[1] = ts_ms
        if b[0] < cost * 1000:
            return False  # denied: refill kept, nothing consumed
        b[0] -= cost * 1000
        return True

    def cleanup(self, now_ms: int, idle_ms: int) -> int:
        """Evict clients whose last request is at or before now_ms - idle_ms (idle >= idle_ms)."""
        idle = [c for c, b in self.buckets.items() if b[1] <= now_ms - idle_ms]
        for c in idle:
            del self.buckets[c]
        return len(idle)


def process(lines: list[str], part: int) -> list[str]:
    """Lines after `PART n`: optional LIMIT/BUCKET header, then `ts [client] [weight]` / CLEANUP."""
    limit, window_ms, capacity, refill = 5, 2000, 5, 2
    body = lines
    if body and body[0].startswith("LIMIT"):
        _, limit, window_ms = body[0].split()
        limit, window_ms, body = int(limit), int(window_ms), body[1:]
    elif body and body[0].startswith("BUCKET"):
        _, capacity, refill = body[0].split()
        capacity, refill, body = int(capacity), int(refill), body[1:]
    limiter = TokenBucket(capacity, refill) if part == 4 else RateLimiter(limit, window_ms)
    out = []
    for ln in body:
        f = ln.split()
        if f[0] == "CLEANUP":
            out.append(f"EVICTED {limiter.cleanup(int(f[1]), int(f[2]))}")
            continue
        ts = int(f[0])
        client = f[1] if len(f) > 1 and part >= 2 else "-"  # Part 1: one global window
        weight = int(f[2]) if len(f) > 2 and part >= 3 else 1
        try:
            out.append("ALLOW" if limiter.allow(client, ts, weight) else "DENY")
        except ValueError:
            out.append("ERROR")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = process(lines[1:], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
