"""pc09 Parallel Courses III -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: `relations` are 1-based [prevCourse, nextCourse] pairs, `time` is 0-based
(time[i] is course i+1's duration). Must be iterative -- LC's own stress tests chain 5*10^4 courses.
"""

from __future__ import annotations

import sys


def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    """Part1 (LC 2050): minimum months to finish all n courses.
    Raise ValueError for a malformed input or a cycle in `relations`."""
    # TODO
    return 0


def critical_path(n: int, relations: list[list[int]], time: list[int]) -> tuple[int, list[int]]:
    """Part2: (minimum_time, one lexicographically smallest critical path, 1-based course ids)."""
    # TODO
    return 0, []


def part1(lines: list[str]) -> list[str]:
    """'n m' / m relation lines 'u v' / one line of n times -> one line: minimum_time."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input -> line 1 minimum_time, line 2 the critical path course ids space-separated."""
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
