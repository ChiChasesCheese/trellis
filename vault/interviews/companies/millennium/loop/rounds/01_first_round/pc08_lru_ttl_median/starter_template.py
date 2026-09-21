"""pc08 LRU Cache + TTL + Median From Stream -- YOUR implementation. Run tests with IMPL=starter.

Two classic designs: an O(1) LRU cache (two implementations that must behave identically), a TTL
extension of it, and a running-median structure over two heaps.
"""

from __future__ import annotations

import sys
import time


class LRUCache:
    """Part1: O(1) get/put via collections.OrderedDict."""

    def __init__(self, capacity: int) -> None:
        # TODO
        self.capacity = capacity

    def get(self, key: int) -> int:
        """Return the value, marking key most-recently-used; -1 if absent."""
        # TODO
        return -1

    def put(self, key: int, value: int) -> None:
        """Insert/update; evict the least-recently-used entry if over capacity."""
        # TODO
        raise NotImplementedError


class LRUCacheLinked:
    """Part1: same behaviour as LRUCache, via a hand-rolled doubly linked list + dict."""

    def __init__(self, capacity: int) -> None:
        # TODO
        self.capacity = capacity

    def get(self, key: int) -> int:
        # TODO
        return -1

    def put(self, key: int, value: int) -> None:
        # TODO
        raise NotImplementedError


class LRUCacheTTL:
    """Part2: LRUCache plus an optional absolute TTL per entry (deadline = clock() + ttl at put
    time; get() never postpones it). clock is injectable (default time.monotonic)."""

    def __init__(self, capacity: int, clock=time.monotonic) -> None:
        # TODO
        self.capacity = capacity
        self._clock = clock

    def get(self, key: int) -> int:
        """Expired entries behave as absent (-1), lazily evicted on this call."""
        # TODO
        return -1

    def put(self, key: int, value: int, ttl: float | None = None) -> None:
        """ttl is seconds from now; None means no expiry. Capacity eviction is independent of
        TTL and always evicts the least-recently-used entry."""
        # TODO
        raise NotImplementedError


class MedianStream:
    """Part3 (LC 295): running median via a max-heap (lower half) + min-heap (upper half)."""

    def __init__(self) -> None:
        # TODO
        pass

    def add(self, num: int | float) -> None:
        # TODO
        raise NotImplementedError

    def median(self) -> float:
        """ValueError on an empty stream."""
        # TODO
        return 0.0


def part1(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then 'PUT <k> <v>' / 'GET <k>'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then 'PUT <k> <v> <ttl|->' / 'GET <k>' / 'TICK <n>'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """ops: 'ADD <num>' / 'MEDIAN'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
