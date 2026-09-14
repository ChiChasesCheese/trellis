"""q22 Dropped Requests -- reference solution.

Classic "rate limiter" / HackerRank "Dropped Requests" shape. requestTimes arrives in
nondecreasing order (whole seconds). A request is rejected (dropped) if it would push any of
three rolling windows over its limit:
  - more than 3 requests in the SAME second (i.e. it's the 4th+ at that exact timestamp)
  - more than 20 requests in the trailing 10-second window [t-9, t]
  - more than 60 requests in the trailing 60-second window [t-59, t]

Part1 (the classic reading, stated explicitly as our choice): the windows count EVERY arrival,
whether or not it was itself dropped -- a dropped request still "used up" its slot in the
second/10s/60s windows for the requests that come after it. This is the standard textbook
version of the problem.

Part2 (reconstructed): the alternative reading -- only ACCEPTED requests count toward the
windows, so a dropped request leaves no trace for later requests. This changes results whenever
back-to-back drops occur, because later requests then see smaller window counts and may be let
through where Part1 would still drop them.

Both run in O(n) amortized: three monotonic pointers/deques, each timestamp added and removed
from a window at most once.
"""

from __future__ import annotations

import sys
from collections import deque


def _validate(request_times: list[int]) -> None:
    prev = None
    for t in request_times:
        if t < 0:
            raise ValueError(f"request time must be >= 0: {t}")
        if prev is not None and t < prev:
            raise ValueError("requestTimes must be nondecreasing")
        prev = t


# --------------------------------------------------------------------------- Part 1
def dropped_requests_count_all(request_times: list[int]) -> list[int]:
    """Windows count ALL arrivals (dropped or not). Returns the dropped timestamps, in order."""
    _validate(request_times)
    dropped: list[int] = []
    win10: deque[int] = deque()
    win60: deque[int] = deque()
    last_time = None
    same_second_count = 0

    for t in request_times:
        win10.append(t)
        while win10[0] < t - 9:
            win10.popleft()
        win60.append(t)
        while win60[0] < t - 59:
            win60.popleft()
        if t == last_time:
            same_second_count += 1
        else:
            last_time = t
            same_second_count = 1

        if same_second_count > 3 or len(win10) > 20 or len(win60) > 60:
            dropped.append(t)
    return dropped


# --------------------------------------------------------------------------- Part 2
def dropped_requests_count_accepted_only(request_times: list[int]) -> list[int]:
    """Windows count only ACCEPTED arrivals -- a dropped request leaves no trace for requests
    that come after it. Returns the dropped timestamps, in order."""
    _validate(request_times)
    dropped: list[int] = []
    win10: deque[int] = deque()
    win60: deque[int] = deque()
    last_time = None
    same_second_count = 0

    for t in request_times:
        while win10 and win10[0] < t - 9:
            win10.popleft()
        while win60 and win60[0] < t - 59:
            win60.popleft()
        tentative_same = (same_second_count + 1) if t == last_time else 1

        if tentative_same > 3 or len(win10) + 1 > 20 or len(win60) + 1 > 60:
            dropped.append(t)
            continue

        # accept: this request now occupies a slot in every window for future requests
        win10.append(t)
        win60.append(t)
        if t == last_time:
            same_second_count = tentative_same
        else:
            last_time = t
            same_second_count = 1
    return dropped


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> list[int]:
    n = int(lines[0]) if lines else 0
    return list(map(int, lines[1].split())) if n else []


def part1(lines: list[str]) -> list[str]:
    """'n' / n nondecreasing timestamps -> dropped timestamps, in order (windows count all
    arrivals)."""
    times = _read(lines)
    return [str(x) for x in dropped_requests_count_all(times)]


def part2(lines: list[str]) -> list[str]:
    """same input -> dropped timestamps, in order (windows count only accepted arrivals)."""
    times = _read(lines)
    return [str(x) for x in dropped_requests_count_accepted_only(times)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
