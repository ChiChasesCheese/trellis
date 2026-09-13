"""od08 LRU/TTL/Two-Tier Cache -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: TTL's half-open validity window, the "expired entries are
free space" eviction rule, and TwoTierCache's promotion/demotion/discard chain.
"""

from __future__ import annotations

import sys
from typing import Hashable

Key = Hashable


class LRUCache:
    def __init__(self, capacity: int) -> None:
        pass  # TODO: O(1) get/put -- a dict + a structure that supports O(1) move-to-MRU

    def get(self, key: Key) -> int:
        """-1 if missing. A hit marks key as most-recently-used."""
        raise NotImplementedError  # TODO

    def put(self, key: Key, value: int) -> None:
        """Insert or update (marks MRU either way). Evict the LRU entry if now over capacity."""
        raise NotImplementedError  # TODO


class TTLCache:
    def __init__(self, capacity: int) -> None:
        pass  # TODO

    def get(self, key: Key, now: int) -> int:
        """-1 if missing OR now >= its expiry (half-open: valid for [put_time, put_time+ttl)).
        A now-expired entry is lazily removed by this call. A hit marks key as MRU."""
        raise NotImplementedError  # TODO

    def put(self, key: Key, value: int, now: int, ttl: int) -> None:
        """Sets/overwrites key's value and expiry (now + ttl), marks MRU. If now over capacity,
        first free space by dropping any already-expired entries; only fall back to evicting the
        LRU *valid* entry if that isn't enough."""
        raise NotImplementedError  # TODO


class TwoTierCache:
    def __init__(self, hot_capacity: int, cold_capacity: int) -> None:
        pass  # TODO: two independent LRU tiers

    def get(self, key: Key) -> int:
        """Hot hit -> mark MRU in hot, return. Cold hit -> PROMOTE (remove from cold, insert
        into hot as MRU, demoting hot's LRU entry to cold if that overflows hot -- which may in
        turn discard cold's LRU entry if that overflows cold). Miss in both -> -1."""
        raise NotImplementedError  # TODO

    def put(self, key: Key, value: int) -> None:
        """A brand-new key always lands in hot (as MRU), same overflow chain as a promotion.
        An existing key (hot or cold) is updated and treated as an access (same as get, but with
        a new value)."""
        raise NotImplementedError  # TODO


def part1(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then one GET/PUT per line, driving a fresh LRUCache."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then 'GET <key> <now>' / 'PUT <key> <value> <now> <ttl>' per
    line, driving a fresh TTLCache."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <hot>,<cold>', then one GET/PUT per line, driving a fresh
    TwoTierCache."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
