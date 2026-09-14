"""od08 LRU/TTL/Two-Tier Cache -- reference solution.

`_LRUStore` is a small internal helper (dict + insertion-order tracking via OrderedDict) shared
by all three public classes: O(1) MRU-touch (`get`/`set_mru`), O(1) LRU-eviction (`pop_lru`), and
O(1) removal. LRUCache is a thin wrapper. TTLCache stores (value, expiry) pairs and, on overflow,
prefers freeing space by dropping already-expired entries before falling back to a true LRU
eviction of a still-valid one. TwoTierCache is two independent _LRUStore instances: promotion
moves an entry cold -> hot; any resulting hot overflow demotes hot's LRU entry to cold; any
resulting cold overflow discards cold's LRU entry outright.
"""

from __future__ import annotations

import sys
from collections import OrderedDict
from typing import Hashable

Key = Hashable


class _LRUStore:
    """key -> value, ordered oldest (LRU) -> newest (MRU) access."""

    def __init__(self) -> None:
        self._data: OrderedDict[Key, object] = OrderedDict()

    def __contains__(self, key: Key) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)  # LRU -> MRU order

    def peek(self, key: Key):
        return self._data[key]

    def get(self, key: Key):
        value = self._data[key]
        self._data.move_to_end(key)
        return value

    def set_mru(self, key: Key, value) -> None:
        self._data[key] = value
        self._data.move_to_end(key)

    def remove(self, key: Key) -> None:
        del self._data[key]

    def pop_lru(self):
        return self._data.popitem(last=False)


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._store: _LRUStore = _LRUStore()

    def get(self, key: Key) -> int:
        if key not in self._store:
            return -1
        return self._store.get(key)

    def put(self, key: Key, value: int) -> None:
        self._store.set_mru(key, value)
        if len(self._store) > self._capacity:
            self._store.pop_lru()


class TTLCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._store: _LRUStore = _LRUStore()

    def _expired(self, key: Key, now: int) -> bool:
        _, expire_at = self._store.peek(key)
        return now >= expire_at

    def get(self, key: Key, now: int) -> int:
        if key not in self._store:
            return -1
        if self._expired(key, now):
            self._store.remove(key)
            return -1
        value, _expire_at = self._store.get(key)
        return value

    def put(self, key: Key, value: int, now: int, ttl: int) -> None:
        self._store.set_mru(key, (value, now + ttl))
        while len(self._store) > self._capacity:
            expired_key = self._find_any_expired(now)
            if expired_key is not None:
                self._store.remove(expired_key)
            else:
                self._store.pop_lru()

    def _find_any_expired(self, now: int):
        for key in self._store:
            if self._expired(key, now):
                return key
        return None


class TwoTierCache:
    def __init__(self, hot_capacity: int, cold_capacity: int) -> None:
        self._hot_capacity = hot_capacity
        self._cold_capacity = cold_capacity
        self._hot: _LRUStore = _LRUStore()
        self._cold: _LRUStore = _LRUStore()

    def get(self, key: Key) -> int:
        if key in self._hot:
            return self._hot.get(key)
        if key in self._cold:
            value = self._cold.peek(key)
            self._cold.remove(key)
            self._insert_hot(key, value)
            return value
        return -1

    def put(self, key: Key, value: int) -> None:
        if key in self._cold:
            self._cold.remove(key)
        self._insert_hot(key, value)

    def _insert_hot(self, key: Key, value) -> None:
        self._hot.set_mru(key, value)
        if len(self._hot) > self._hot_capacity:
            demoted_key, demoted_value = self._hot.pop_lru()
            self._insert_cold(demoted_key, demoted_value)

    def _insert_cold(self, key: Key, value) -> None:
        self._cold.set_mru(key, value)
        if len(self._cold) > self._cold_capacity:
            self._cold.pop_lru()  # discarded entirely


# ---------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    capacity = int(lines[0].split()[1])
    cache = LRUCache(capacity)
    out: list[str] = []
    for line in lines[1:]:
        fields = line.split()
        if fields[0] == "GET":
            out.append(str(cache.get(fields[1])))
        else:  # PUT
            cache.put(fields[1], int(fields[2]))
    return out


def part2(lines: list[str]) -> list[str]:
    capacity = int(lines[0].split()[1])
    cache = TTLCache(capacity)
    out: list[str] = []
    for line in lines[1:]:
        fields = line.split()
        if fields[0] == "GET":
            out.append(str(cache.get(fields[1], int(fields[2]))))
        else:  # PUT
            cache.put(fields[1], int(fields[2]), int(fields[3]), int(fields[4]))
    return out


def part3(lines: list[str]) -> list[str]:
    hot_s, cold_s = lines[0].split()[1].split(",")
    cache = TwoTierCache(int(hot_s), int(cold_s))
    out: list[str] = []
    for line in lines[1:]:
        fields = line.split()
        if fields[0] == "GET":
            out.append(str(cache.get(fields[1])))
        else:  # PUT
            cache.put(fields[1], int(fields[2]))
    return out


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
