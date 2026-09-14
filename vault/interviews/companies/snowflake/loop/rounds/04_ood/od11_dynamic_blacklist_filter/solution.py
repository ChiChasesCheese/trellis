"""od11 Dynamic Blacklist Filter System -- reference solution.

Source (MED, TrueInterview via kevin-2023-code/Tech-Interview-Questions "Dynamic Blacklist
Filter System", LLD, reported 2026-06; also a title-only 1point3acres interview-index hit,
"Dynamic Blacklist Filter System", no body text -- see problem.md Sources). Only the shape
("two streams -- filter mutations and input values -- decide whether each input value should
pass") is confirmed by the preview; every rule below that (tie-break ordering, reference
counts, wildcard prefixes, the concurrency model) is reconstructed and labelled in problem.md.

Part1: single-threaded add(v)/remove(v)/offer(v) plus a merged event-log processor ordered by
timestamp, ties broken filter-mutations-before-inputs (reconstructed).
Part2: reference-counted add/remove from multiple owners (a value stays blocked while ANY
owner still blocks it) plus prefix/wildcard patterns like "10.0.*".
Part3: thread safety -- concurrent producers on both streams, read-write lock (a single
threading.Lock here, since Python's GIL plus a single mutex is what "readers see a consistent
snapshot" needs at this scale); correctness is checked against a sequential replay of the exact
same operations recorded, in commit order, under that same lock.
"""

from __future__ import annotations

import sys
import threading


# --------------------------------------------------------------------------- Part 1
class BlacklistFilter:
    """Single-threaded exact-value blacklist. add/remove are set membership; offer(v) reports
    whether v is currently allowed (True) or blacklisted (False)."""

    def __init__(self) -> None:
        self._blocked: set[str] = set()

    def add(self, v: str) -> None:
        self._blocked.add(v)

    def remove(self, v: str) -> None:
        self._blocked.discard(v)

    def offer(self, v: str) -> bool:
        return v not in self._blocked


def process_events(events: list[tuple[int, str, str]]) -> list[bool]:
    """events: list of (timestamp, kind, value). kind is 'ADD' / 'REMOVE' / 'IN'. Stable-sort by
    timestamp; at equal timestamps filter mutations (ADD/REMOVE) are applied before inputs (IN)
    so an input arriving "at the same instant" as a mutation always sees the post-mutation state
    -- (reconstructed) tie-break, stated because the source preview gives no ordering rule.
    Returns one bool per IN event, in the order they appear in the *sorted* stream, True meaning
    "passed" (not blacklisted)."""
    kind_rank = {"ADD": 0, "REMOVE": 0, "IN": 1}
    ordered = sorted(events, key=lambda e: (e[0], kind_rank[e[1]]))
    f = BlacklistFilter()
    out: list[bool] = []
    for _ts, kind, value in ordered:
        if kind == "ADD":
            f.add(value)
        elif kind == "REMOVE":
            f.remove(value)
        else:
            out.append(f.offer(value))
    return out


# --------------------------------------------------------------------------- Part 2
class RefCountedPatternFilter:
    """Reconstructed extension: multiple owners can each ADD/REMOVE the same value or pattern;
    a value stays blocked while *any* owner still blocks it (reference counting, not a boolean
    flag). Patterns are prefix/wildcard strings ending in '*' (e.g. "10.0.*"), matched by simple
    prefix comparison against the literal value offered -- exact values and patterns share one
    reference-counted map keyed by the literal filter string."""

    def __init__(self) -> None:
        self._owned: set[tuple[str, str]] = set()
        self._refcount: dict[str, int] = {}

    def add(self, owner: str, pattern: str) -> None:
        key = (owner, pattern)
        # each (owner, pattern) pair contributes at most one reference; repeated ADD by the same
        # owner for the same pattern is idempotent (does not inflate the refcount further).
        if key in self._owned:
            return
        self._owned.add(key)
        self._refcount[pattern] = self._refcount.get(pattern, 0) + 1

    def remove(self, owner: str, pattern: str) -> None:
        key = (owner, pattern)
        if key not in self._owned:
            return  # this owner never blocked this pattern: no-op, never raises
        self._owned.discard(key)
        self._refcount[pattern] -= 1
        if self._refcount[pattern] <= 0:
            del self._refcount[pattern]

    def offer(self, v: str) -> bool:
        for pattern in self._refcount:
            if pattern.endswith("*"):
                if v.startswith(pattern[:-1]):
                    return False
            elif pattern == v:
                return False
        return True


def process_events_refcounted(events: list[tuple[int, str, str, str]]) -> list[bool]:
    """events: (timestamp, kind, owner, value_or_pattern) for ADD/REMOVE, or
    (timestamp, 'IN', '', value) for inputs. Same tie-break as Part1 (mutations before inputs at
    equal timestamp)."""
    kind_rank = {"ADD": 0, "REMOVE": 0, "IN": 1}
    ordered = sorted(events, key=lambda e: (e[0], kind_rank[e[1]]))
    f = RefCountedPatternFilter()
    out: list[bool] = []
    for _ts, kind, owner, value in ordered:
        if kind == "ADD":
            f.add(owner, value)
        elif kind == "REMOVE":
            f.remove(owner, value)
        else:
            out.append(f.offer(value))
    return out


# --------------------------------------------------------------------------- Part 3
class ThreadSafeBlacklistFilter:
    """Reconstructed: same reference-counted/pattern semantics as Part2, safe for concurrent
    producers on both streams. A single RLock guards every mutation and every read, giving
    readers a consistent snapshot (copy-on-write would also satisfy the spec; a lock is simpler
    to reason about and cheap at this scale -- see problem.md follow-ups for the trade-off)."""

    def __init__(self) -> None:
        self._inner = RefCountedPatternFilter()
        self._lock = threading.RLock()
        self._log: list[tuple[int, str, str, str]] = []  # linearization: (seq, kind, owner, val)
        self._seq = 0

    def add(self, owner: str, pattern: str) -> None:
        with self._lock:
            self._inner.add(owner, pattern)
            self._log.append((self._seq, "ADD", owner, pattern))
            self._seq += 1

    def remove(self, owner: str, pattern: str) -> None:
        with self._lock:
            self._inner.remove(owner, pattern)
            self._log.append((self._seq, "REMOVE", owner, pattern))
            self._seq += 1

    def offer(self, v: str) -> bool:
        with self._lock:
            result = self._inner.offer(v)
            self._log.append((self._seq, "IN", "", v))
            self._seq += 1
            return result

    def linearization_log(self) -> list[tuple[int, str, str, str]]:
        """The exact order operations were actually applied, for cross-checking against a
        sequential replay (see test_od11.py's concurrency test)."""
        with self._lock:
            return list(self._log)


def replay_sequential(log: list[tuple[int, str, str, str]]) -> list[bool]:
    """Re-run a recorded linearization sequentially and return the IN results in log order --
    used to prove a concurrent run's observed outputs match SOME valid interleaving."""
    f = RefCountedPatternFilter()
    out: list[bool] = []
    for _seq, kind, owner, value in log:
        if kind == "ADD":
            f.add(owner, value)
        elif kind == "REMOVE":
            f.remove(owner, value)
        else:
            out.append(f.offer(value))
    return out


# --------------------------------------------------------------------------- command stream
def _part1_lines(lines: list[str]) -> list[str]:
    events: list[tuple[int, str, str]] = []
    for line in lines:
        fields = line.split()
        ts = int(fields[0])
        kind = fields[1]
        value = fields[2]
        events.append((ts, kind, value))
    results = process_events(events)
    return ["true" if r else "false" for r in results]


def _part2_lines(lines: list[str]) -> list[str]:
    events: list[tuple[int, str, str, str]] = []
    for line in lines:
        fields = line.split()
        ts = int(fields[0])
        kind = fields[1]
        if kind == "IN":
            events.append((ts, "IN", "", fields[2]))
        else:
            events.append((ts, kind, fields[2], fields[3]))
    results = process_events_refcounted(events)
    return ["true" if r else "false" for r in results]


def _part3_lines(lines: list[str]) -> list[str]:
    """Single-threaded command replay through the thread-safe class (proves it behaves
    identically to Part2 when there is no actual concurrency); real concurrency is exercised
    directly against the class in tests, not via this line format."""
    f = ThreadSafeBlacklistFilter()
    out: list[str] = []
    for line in lines:
        fields = line.split()
        ts_kind = fields[1]
        if ts_kind == "ADD":
            f.add(fields[2], fields[3])
        elif ts_kind == "REMOVE":
            f.remove(fields[2], fields[3])
        else:
            out.append("true" if f.offer(fields[2]) else "false")
    return out


def part1(lines: list[str]) -> list[str]:
    return _part1_lines(lines)


def part2(lines: list[str]) -> list[str]:
    return _part2_lines(lines)


def part3(lines: list[str]) -> list[str]:
    return _part3_lines(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
