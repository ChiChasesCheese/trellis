"""od04 Rate Limiter -- reference solution.

Part1's RateLimiter is a plain deque-backed sliding-window log: purge entries that have aged out
of (t - window, t], then accept iff the remainder is under `limit`.

Part2/Part3 share one core routine, `_advance`: given a candidate time `t` and, per rule, a
deque of previously-granted timestamps (invariant: never holds more than that rule's `limit`
entries, because an entry is only appended once a check confirmed room), repeatedly push `t`
forward until every rule simultaneously has room. Because appending only ever happens after
confirming room, each rule's deque never exceeds its own `limit` in length, so indexing into it
is cheap regardless of how many requests have been processed overall.
"""

from __future__ import annotations

import sys
import threading
from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window = window_seconds
        self._accepted: deque[int] = deque()

    def allow(self, t: int) -> bool:
        while self._accepted and self._accepted[0] <= t - self.window:
            self._accepted.popleft()
        if len(self._accepted) < self.limit:
            self._accepted.append(t)
            return True
        return False


def accept_requests(request_times: list[int], limit: int, window_seconds: int) -> list[bool]:
    limiter = RateLimiter(limit, window_seconds)
    return [limiter.allow(t) for t in request_times]


def _advance(t: int, rules: list[tuple[int, int]], granted_per_rule: list[deque]) -> int:
    """Earliest time >= t at which every rule simultaneously has room, given each rule's deque
    of currently-granted timestamps (mutated in place: expired entries are purged)."""
    while True:
        advanced = False
        for (limit, window), granted in zip(rules, granted_per_rule):
            while granted and granted[0] <= t - window:
                granted.popleft()
            if len(granted) >= limit:
                idx = len(granted) - limit
                new_t = granted[idx] + window
                if new_t > t:
                    t = new_t
                    advanced = True
        if not advanced:
            return t


def simulate_rate_limiter(
    requests: list[tuple[int, int]], rules: list[tuple[int, int]]
) -> list[int]:
    granted_per_rule: list[deque] = [deque() for _ in rules]
    prev_start: int | None = None
    results: list[int] = []
    for arrival, success_flag in requests:
        t = arrival if prev_start is None else max(arrival, prev_start)
        t = _advance(t, rules, granted_per_rule)
        prev_start = t
        if success_flag:
            for granted in granted_per_rule:
                granted.append(t)
        results.append(t)
    return results


class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int, int]]) -> None:
        self._rules = list(rules)
        self._granted_per_rule: list[deque] = [deque() for _ in self._rules]
        self._prev_start: int | None = None
        self._lock = threading.Lock()

    def try_acquire(self, arrival_time: int) -> int:
        with self._lock:
            t = arrival_time if self._prev_start is None else max(arrival_time, self._prev_start)
            t = _advance(t, self._rules, self._granted_per_rule)
            self._prev_start = t
            for granted in self._granted_per_rule:
                granted.append(t)
            return t


# ---------------------------------------------------------------------- line-driven wrappers
def _parse_rules(line: str) -> list[tuple[int, int]]:
    body = line.split(" ", 1)[1]
    rules = []
    for piece in body.split(","):
        limit_s, window_s = piece.split(":")
        rules.append((int(limit_s), int(window_s)))
    return rules


def part1(lines: list[str]) -> list[str]:
    limit = int(lines[0].split()[1])
    window = int(lines[1].split()[1])
    limiter = RateLimiter(limit, window)
    return [str(limiter.allow(int(line))) for line in lines[2:]]


def part2(lines: list[str]) -> list[str]:
    rules = _parse_rules(lines[0])
    requests = []
    for line in lines[1:]:
        t_s, f_s = line.split(":")
        requests.append((int(t_s), int(f_s)))
    return [str(s) for s in simulate_rate_limiter(requests, rules)]


def part3(lines: list[str]) -> list[str]:
    rules = _parse_rules(lines[0])
    limiter = MultiRuleRateLimiter(rules)
    return [str(limiter.try_acquire(int(line))) for line in lines[1:]]


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
