"""q22 Dropped Requests -- YOUR implementation. Run tests against this file with IMPL=starter.

requestTimes arrives nondecreasing (whole seconds). Reject (drop) a request if it would push:
same-second count > 3, OR the trailing 10s window > 20, OR the trailing 60s window > 60.
Part1: windows count ALL arrivals (dropped included). Part2 (reconstructed): windows count only
ACCEPTED arrivals.
"""

from __future__ import annotations

import sys


def dropped_requests_count_all(request_times: list[int]) -> list[int]:
    """Part1: windows count every arrival, dropped or not. Returns dropped timestamps in order."""
    # TODO
    return []


def dropped_requests_count_accepted_only(request_times: list[int]) -> list[int]:
    """Part2: windows count only accepted arrivals. Returns dropped timestamps in order."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'n' / n nondecreasing timestamps -> dropped timestamps, in order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> dropped timestamps, in order (accepted-only windows)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
