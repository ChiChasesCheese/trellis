"""od04 Rate Limiter -- YOUR implementation. Run pytest against this file with IMPL=starter.

See problem.md for the full contract: the half-open sliding window, the multi-rule FIFO
simulation (including the success_flag=0 "waits for capacity, consumes no slot" rule), and the
thread-safety requirement for try_acquire.
"""

from __future__ import annotations

import sys
from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        pass  # TODO: limit, window, and a deque of accepted timestamps

    def allow(self, t: int) -> bool:
        """Half-open window (t - window_seconds, t]. Purge expired timestamps, then accept iff
        fewer than `limit` remain; a rejected request must not occupy a slot."""
        raise NotImplementedError  # TODO


def accept_requests(request_times: list[int], limit: int, window_seconds: int) -> list[bool]:
    """Replay request_times (non-decreasing) through a fresh RateLimiter."""
    # TODO
    return []


def simulate_rate_limiter(
    requests: list[tuple[int, int]], rules: list[tuple[int, int]]
) -> list[int]:
    """Process (arrival_time, success_flag) requests strictly in FIFO order. Each request's
    actual start time is the earliest time >= max(arrival_time, previous start time) at which
    EVERY rule has room. success_flag == 1 requests consume a slot in every rule once granted;
    success_flag == 0 requests still wait for that moment but consume nothing."""
    # TODO
    return []


class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int, int]]) -> None:
        pass  # TODO: rules, per-rule granted-timestamp deques, a lock

    def try_acquire(self, arrival_time: int) -> int:
        """Same FIFO + all-rules-satisfied logic as simulate_rate_limiter's success_flag=1 case,
        but as a stateful, thread-safe, incrementally-called method: the whole
        check-then-record step must be atomic under concurrent callers."""
        raise NotImplementedError  # TODO


def _parse_rules(line: str) -> list[tuple[int, int]]:
    body = line.split(" ", 1)[1]
    rules = []
    for piece in body.split(","):
        limit_s, window_s = piece.split(":")
        rules.append((int(limit_s), int(window_s)))
    return rules


def part1(lines: list[str]) -> list[str]:
    """lines[0] = 'LIMIT <n>', lines[1] = 'WINDOW <n>', then one timestamp per line -> one
    True/False per line via RateLimiter.allow."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'RULES l1:w1[,l2:w2...]', then one '<t>:<success_flag>' per line -> one actual
    start time per line via simulate_rate_limiter."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'RULES l1:w1[,l2:w2...]', then one timestamp per line -> one actual start time
    per line via MultiRuleRateLimiter.try_acquire (single-threaded driver; the concurrency
    guarantee is exercised directly against the class with real threads in test_od04.py)."""
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
