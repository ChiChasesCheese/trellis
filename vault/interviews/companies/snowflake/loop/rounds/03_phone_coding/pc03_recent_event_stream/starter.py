"""pc03 Recent Event Stream -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: Part1 keeps a COUNT-based window (the most recent `m`
events); Part2 keeps a TIME-based window (events within `window_seconds` of the latest recorded
timestamp, half-open like od04's RateLimiter). Both support `record`/`count`/`top`.
"""

from __future__ import annotations

import sys


class RecentEventStream:
    """Part1: retain only the `m` most-recently recorded events."""

    def __init__(self, m: int) -> None:
        pass  # TODO: m, a deque of (ts, key), a key -> count in the current window

    def record(self, ts: int, key: str) -> None:
        raise NotImplementedError  # TODO

    def count(self, ts: int) -> int:
        """Distinct keys among retained events with timestamp strictly before `ts`."""
        raise NotImplementedError  # TODO

    def top(self) -> str:
        """Most frequent key in the retained window; lexicographically smallest on a tie.
        Empty window -> ""."""
        raise NotImplementedError  # TODO


def process_recent_event_stream(operations: list[tuple], m: int) -> list[str]:
    """operations: list of ("record", ts, key) / ("count", ts) / ("top",). Returns one string
    per count/top operation, in order; record operations produce no output."""
    # TODO
    return []


class RecentEventStreamByTime:
    """Part2: retain events within `(latest_ts - window_seconds, latest_ts]` of the most
    recently recorded timestamp."""

    def __init__(self, window_seconds: int) -> None:
        pass  # TODO

    def record(self, ts: int, key: str) -> None:
        raise NotImplementedError  # TODO

    def count(self, ts: int) -> int:
        raise NotImplementedError  # TODO

    def top(self) -> str:
        raise NotImplementedError  # TODO


def process_recent_event_stream_by_time(operations: list[tuple], window_seconds: int) -> list[str]:
    # TODO
    return []


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
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'WINDOW <window_seconds>', then ops in the same format as part1."""
    # TODO
    return []


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
