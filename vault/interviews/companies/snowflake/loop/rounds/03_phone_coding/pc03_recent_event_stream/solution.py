"""pc03 Recent Event Stream -- reference solution.

Both parts keep a deque of (ts, key) for the currently retained window plus a Counter of
key -> count within that window, so `record` is amortised O(1) and `top` is O(distinct keys in
the window) <= O(window cap). `count(ts)` scans the (small, capped) window once per call --
that's the expected phone-screen-level answer, since the window is bounded by `m` /
`window_seconds` regardless of how many events have streamed through overall.

Part1's window is COUNT-based (keep the most recent `m` events, no matter their timestamps).
Part2's window is TIME-based (keep events within `(latest_ts - window_seconds, latest_ts]`,
same half-open convention as od04's RateLimiter). Streams are assumed to arrive in non-decreasing
timestamp order, same assumption as every other streaming problem in this kit.
"""

from __future__ import annotations

import sys
from collections import Counter, deque


class RecentEventStream:
    """Part1: retain only the `m` most-recently recorded events."""

    def __init__(self, m: int) -> None:
        self.m = m
        self._window: deque[tuple[int, str]] = deque()
        self._counts: Counter[str] = Counter()

    def record(self, ts: int, key: str) -> None:
        self._window.append((ts, key))
        self._counts[key] += 1
        if len(self._window) > self.m:
            old_ts, old_key = self._window.popleft()
            self._counts[old_key] -= 1
            if self._counts[old_key] == 0:
                del self._counts[old_key]

    def count(self, ts: int) -> int:
        """Distinct keys among retained events with timestamp strictly before `ts`."""
        return len({k for t, k in self._window if t < ts})

    def top(self) -> str:
        """Most frequent key in the retained window; lexicographically smallest on a tie.
        Empty window -> "" (no exception -- a query on a stream that hasn't recorded anything
        yet is a normal, expected state, not an error)."""
        if not self._counts:
            return ""
        best = max(self._counts.values())
        return min(k for k, c in self._counts.items() if c == best)


def process_recent_event_stream(operations: list[tuple], m: int) -> list[str]:
    """operations: list of ("record", ts, key) / ("count", ts) / ("top",). Returns one string
    per count/top operation, in order; record operations produce no output."""
    stream = RecentEventStream(m)
    out: list[str] = []
    for op in operations:
        kind = op[0]
        if kind == "record":
            stream.record(op[1], op[2])
        elif kind == "count":
            out.append(str(stream.count(op[1])))
        elif kind == "top":
            out.append(stream.top())
        else:
            raise ValueError(f"unknown operation {kind!r}")
    return out


class RecentEventStreamByTime:
    """Part2: retain events within `(latest_ts - window_seconds, latest_ts]` of the most
    recently recorded timestamp (half-open, same boundary convention as od04's RateLimiter)."""

    def __init__(self, window_seconds: int) -> None:
        self.window_seconds = window_seconds
        self._window: deque[tuple[int, str]] = deque()
        self._counts: Counter[str] = Counter()

    def record(self, ts: int, key: str) -> None:
        # Purge BEFORE appending (same order as od04's RateLimiter.allow): the new event must
        # never be compared against itself, which matters exactly at window_seconds == 0.
        while self._window and self._window[0][0] <= ts - self.window_seconds:
            old_ts, old_key = self._window.popleft()
            self._counts[old_key] -= 1
            if self._counts[old_key] == 0:
                del self._counts[old_key]
        self._window.append((ts, key))
        self._counts[key] += 1

    def count(self, ts: int) -> int:
        return len({k for t, k in self._window if t < ts})

    def top(self) -> str:
        if not self._counts:
            return ""
        best = max(self._counts.values())
        return min(k for k, c in self._counts.items() if c == best)


def process_recent_event_stream_by_time(operations: list[tuple], window_seconds: int) -> list[str]:
    stream = RecentEventStreamByTime(window_seconds)
    out: list[str] = []
    for op in operations:
        kind = op[0]
        if kind == "record":
            stream.record(op[1], op[2])
        elif kind == "count":
            out.append(str(stream.count(op[1])))
        elif kind == "top":
            out.append(stream.top())
        else:
            raise ValueError(f"unknown operation {kind!r}")
    return out


# --------------------------------------------------------------------------- line-driven wrappers
def _parse_ops(lines: list[str]) -> list[tuple]:
    ops = []
    for line in lines:
        parts = line.split()
        kind = parts[0]
        if kind == "RECORD":
            ops.append(("record", int(parts[1]), parts[2]))
        elif kind == "COUNT":
            ops.append(("count", int(parts[1])))
        elif kind == "TOP":
            ops.append(("top",))
        else:
            raise ValueError(f"unknown op line {line!r}")
    return ops


def part1(lines: list[str]) -> list[str]:
    """lines[0] = 'M <m>', then one op per line: 'RECORD <ts> <key>' / 'COUNT <ts>' / 'TOP'."""
    m = int(lines[0].split()[1])
    return process_recent_event_stream(_parse_ops(lines[1:]), m)


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'WINDOW <window_seconds>', then ops in the same format as part1."""
    window_seconds = int(lines[0].split()[1])
    return process_recent_event_stream_by_time(_parse_ops(lines[1:]), window_seconds)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
