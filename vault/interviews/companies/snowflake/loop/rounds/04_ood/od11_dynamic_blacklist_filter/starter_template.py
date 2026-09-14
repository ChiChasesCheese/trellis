"""od11 Dynamic Blacklist Filter System -- YOUR implementation. Run the tests against this file
with IMPL=starter. See problem.md for every rule (tie-break at equal timestamps, reference
counting across owners, wildcard prefixes, and the linearizable concurrency contract)."""

from __future__ import annotations

import sys
import threading


# --------------------------------------------------------------------------- Part 1
class BlacklistFilter:
    def __init__(self) -> None:
        pass  # TODO

    def add(self, v: str) -> None:
        raise NotImplementedError  # TODO

    def remove(self, v: str) -> None:
        raise NotImplementedError  # TODO: no-op if v is not currently blocked

    def offer(self, v: str) -> bool:
        raise NotImplementedError  # TODO: True = passed, False = blacklisted


def process_events(events: list[tuple[int, str, str]]) -> list[bool]:
    """events: (timestamp, kind, value), kind in {'ADD', 'REMOVE', 'IN'}, NOT necessarily sorted
    by timestamp. TODO: sort by (timestamp, mutation-before-input), replay, return one bool per
    IN event in the sorted order."""
    raise NotImplementedError  # TODO


# --------------------------------------------------------------------------- Part 2
class RefCountedPatternFilter:
    def __init__(self) -> None:
        pass  # TODO

    def add(self, owner: str, pattern: str) -> None:
        raise NotImplementedError  # TODO: idempotent per (owner, pattern)

    def remove(self, owner: str, pattern: str) -> None:
        raise NotImplementedError  # TODO: no-op if this owner never blocked pattern

    def offer(self, v: str) -> bool:
        raise NotImplementedError  # TODO: exact match or prefix ("10.0.*") match, any refcount>0


def process_events_refcounted(events: list[tuple[int, str, str, str]]) -> list[bool]:
    """events: (timestamp, kind, owner, value_or_pattern) for ADD/REMOVE, or
    (timestamp, 'IN', '', value) for inputs."""
    raise NotImplementedError  # TODO


# --------------------------------------------------------------------------- Part 3
class ThreadSafeBlacklistFilter:
    def __init__(self) -> None:
        pass  # TODO

    def add(self, owner: str, pattern: str) -> None:
        raise NotImplementedError  # TODO: thread-safe

    def remove(self, owner: str, pattern: str) -> None:
        raise NotImplementedError  # TODO: thread-safe

    def offer(self, v: str) -> bool:
        raise NotImplementedError  # TODO: thread-safe

    def linearization_log(self) -> list[tuple[int, str, str, str]]:
        raise NotImplementedError  # TODO: the order operations actually took effect


def replay_sequential(log: list[tuple[int, str, str, str]]) -> list[bool]:
    raise NotImplementedError  # TODO: sequential replay of a recorded linearization


# --------------------------------------------------------------------------- command stream
def part1(lines: list[str]) -> list[str]:
    # TODO: parse "<ts> ADD <v>" / "<ts> REMOVE <v>" / "<ts> IN <v>", call process_events,
    # format results as "true"/"false"
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO: parse "<ts> ADD <owner> <pattern>" / "<ts> REMOVE <owner> <pattern>" /
    # "<ts> IN <value>"
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO: same command shape as part2, but replayed through ThreadSafeBlacklistFilter
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
