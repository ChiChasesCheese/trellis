"""pc08 LRU Cache + TTL + Median From Stream -- reference solution.

Two classic designs packed into one 45-min problem, the way QuantVault's Millennium question
list reports them (LRU Cache, Median from a Data Stream, no round labelled -- same family as the
Stripe/Snowflake decks' high-frequency design pair).

Part1 (LC 146, LRU Cache): O(1) get/put. Two behaviourally-identical implementations are given
on purpose, because interviewers ask for both: `LRUCache` wraps `collections.OrderedDict` (the
answer you actually ship), `LRUCacheLinked` hand-rolls a doubly linked list + dict (the answer
interviewers ask for when they want to see you reason about pointers). Both are exercised by the
same behavioural test suite.

Part2: adds an optional TTL per entry. The clock is injected (`clock: Callable[[], float]`,
default `time.monotonic`) so tests can control time exactly. TTL is an ABSOLUTE deadline set at
`put` time (`clock() + ttl`), not a sliding window that `get` extends -- `get`ting an entry marks
it most-recently-used for LRU purposes but never postpones its expiry. Expiry is checked lazily,
on `get`: an expired entry is treated as absent (evicted on the read) and reports the same miss
as a key that was never inserted. Capacity eviction (the actual LRU order) is a SEPARATE
mechanism from TTL expiry: it fires only when `put` pushes the entry count over capacity, and it
evicts the least-recently-used entry regardless of whether it has a TTL, exactly as in Part1.

Part3 (Median From a Data Stream, LC 295): a max-heap for the lower half and a min-heap for the
upper half, rebalanced after every `add` so their sizes differ by at most 1. The median is the
top of the larger heap (odd total) or the average of both tops (even total) -- this is the
textbook reason "why two heaps": it turns an O(n) insert-sorted / O(n log n) full-resort per query
into O(log n) insert and O(1) query.
"""

from __future__ import annotations

import heapq
import sys
import time
from collections import OrderedDict


def _check_capacity(capacity) -> None:
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
        raise ValueError(f"capacity must be a positive int, got {capacity!r}")


def _check_key_value(key, value=0, *, check_value: bool = False) -> None:
    if not isinstance(key, int) or isinstance(key, bool):
        raise ValueError(f"key must be an int, got {key!r}")
    if check_value and (not isinstance(value, int) or isinstance(value, bool)):
        raise ValueError(f"value must be an int, got {value!r}")


# --------------------------------------------------------------------------- Part 1
class LRUCache:
    """O(1) get/put backed by collections.OrderedDict (move_to_end + popitem)."""

    def __init__(self, capacity: int) -> None:
        _check_capacity(capacity)
        self.capacity = capacity
        self._data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        _check_key_value(key)
        if key not in self._data:
            return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: int, value: int) -> None:
        _check_key_value(key, value, check_value=True)
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)  # evict least-recently-used (front of the order)


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: "_Node | None" = None
        self.next: "_Node | None" = None


class LRUCacheLinked:
    """O(1) get/put via a hand-rolled doubly linked list (MRU at the tail, LRU at the head) plus
    a dict[key -> node]. Behaviourally identical to LRUCache -- this is the version interviewers
    ask for when they want to see the pointer bookkeeping, not just `OrderedDict`."""

    def __init__(self, capacity: int) -> None:
        _check_capacity(capacity)
        self.capacity = capacity
        self._nodes: dict[int, _Node] = {}
        self._head = _Node()  # sentinel, .next is the LRU end
        self._tail = _Node()  # sentinel, .prev is the MRU end
        self._head.next = self._tail
        self._tail.prev = self._head

    def _unlink(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_mru(self, node: _Node) -> None:
        last = self._tail.prev
        last.next = node
        node.prev = last
        node.next = self._tail
        self._tail.prev = node

    def get(self, key: int) -> int:
        _check_key_value(key)
        node = self._nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_mru(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        _check_key_value(key, value, check_value=True)
        node = self._nodes.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_mru(node)
            return
        node = _Node(key, value)
        self._nodes[key] = node
        self._push_mru(node)
        if len(self._nodes) > self.capacity:
            lru = self._head.next
            self._unlink(lru)
            del self._nodes[lru.key]


# --------------------------------------------------------------------------- Part 2
class LRUCacheTTL:
    """LRUCache with an optional per-entry TTL. `clock` is injected (default time.monotonic) so
    tests can control time exactly. TTL is an ABSOLUTE deadline set at put time (clock() + ttl),
    not sliding -- get() never postpones expiry, it only checked (lazily) whether the deadline
    has passed. Capacity eviction (LRU order) is separate from TTL expiry and fires on put
    regardless of any entry's TTL, same as Part1."""

    def __init__(self, capacity: int, clock=time.monotonic) -> None:
        _check_capacity(capacity)
        if not callable(clock):
            raise ValueError(f"clock must be callable, got {clock!r}")
        self.capacity = capacity
        self._clock = clock
        self._data: OrderedDict[int, int] = OrderedDict()
        self._expiry: dict[int, float] = {}  # key -> absolute deadline; absent = no TTL

    def _is_expired(self, key: int) -> bool:
        deadline = self._expiry.get(key)
        return deadline is not None and self._clock() >= deadline

    def get(self, key: int) -> int:
        _check_key_value(key)
        if key not in self._data:
            return -1
        if self._is_expired(key):
            del self._data[key]
            del self._expiry[key]
            return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: int, value: int, ttl: float | None = None) -> None:
        _check_key_value(key, value, check_value=True)
        if ttl is not None and (not isinstance(ttl, (int, float)) or isinstance(ttl, bool) or ttl <= 0):
            raise ValueError(f"ttl must be a positive number or None, got {ttl!r}")
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if ttl is None:
            self._expiry.pop(key, None)
        else:
            self._expiry[key] = self._clock() + ttl
        if len(self._data) > self.capacity:
            evict_key, _ = self._data.popitem(last=False)
            self._expiry.pop(evict_key, None)


# --------------------------------------------------------------------------- Part 3
class MedianStream:
    """Running median of a stream of numbers via a max-heap (lower half, negated) + a min-heap
    (upper half), rebalanced after every add so |len(lower) - len(upper)| <= 1."""

    def __init__(self) -> None:
        self._lower: list[float] = []  # max-heap via negation
        self._upper: list[float] = []  # min-heap

    def add(self, num: int | float) -> None:
        if not isinstance(num, (int, float)) or isinstance(num, bool):
            raise ValueError(f"num must be int or float, got {num!r}")
        if self._lower and num <= -self._lower[0]:
            heapq.heappush(self._lower, -num)
        else:
            heapq.heappush(self._upper, num)
        # rebalance: lower may hold at most one more than upper
        if len(self._lower) > len(self._upper) + 1:
            heapq.heappush(self._upper, -heapq.heappop(self._lower))
        elif len(self._upper) > len(self._lower):
            heapq.heappush(self._lower, -heapq.heappop(self._upper))

    def median(self) -> float:
        if not self._lower and not self._upper:
            raise ValueError("median of an empty stream is undefined")
        if len(self._lower) > len(self._upper):
            return float(-self._lower[0])
        return (-self._lower[0] + self._upper[0]) / 2


def _format_median(m: float) -> str:
    """Whole-valued medians print without a decimal point (e.g. '5', not '5.0')."""
    return str(int(m)) if m == int(m) else str(m)


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then 'PUT <k> <v>' (no output) / 'GET <k>' -> int."""
    capacity = int(lines[0].split()[1])
    cache = LRUCache(capacity)
    out: list[str] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "PUT":
            cache.put(int(rest[0]), int(rest[1]))
        elif cmd == "GET":
            out.append(str(cache.get(int(rest[0]))))
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'CAPACITY <n>', then 'PUT <k> <v> <ttl|->' / 'GET <k>' -> int / 'TICK <n>'
    (advances an internal fake clock by n seconds; no real time is used here, so this wrapper is
    fully deterministic)."""
    capacity = int(lines[0].split()[1])
    now = [0.0]
    cache = LRUCacheTTL(capacity, clock=lambda: now[0])
    out: list[str] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "PUT":
            ttl = None if rest[2] == "-" else float(rest[2])
            cache.put(int(rest[0]), int(rest[1]), ttl=ttl)
        elif cmd == "GET":
            out.append(str(cache.get(int(rest[0]))))
        elif cmd == "TICK":
            now[0] += float(rest[0])
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def part3(lines: list[str]) -> list[str]:
    """ops: 'ADD <num>' (no output) / 'MEDIAN' -> formatted number."""
    stream = MedianStream()
    out: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        cmd, *rest = line.split()
        if cmd == "ADD":
            stream.add(float(rest[0]) if "." in rest[0] else int(rest[0]))
        elif cmd == "MEDIAN":
            out.append(_format_median(stream.median()))
        else:
            raise ValueError(f"unknown op {line!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
