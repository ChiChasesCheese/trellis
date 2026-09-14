"""pc05 Max Events II -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: events are [start, end, value] with an INCLUSIVE end; two events can both be
attended only if the later one starts strictly after the earlier one ends.
"""

from __future__ import annotations

import sys


def max_value(events: list[list[int]], k: int) -> int:
    """Part1 (LC 1751): best total value attending at most k non-overlapping events.
    Raise ValueError for an event with start > end or a negative value."""
    # TODO
    return 0


def max_value_with_events(events: list[list[int]], k: int) -> tuple[int, list[int]]:
    """Part2: (best value, one optimal set of ORIGINAL indices in ascending order)."""
    # TODO
    return 0, []


def max_value_unbounded(events: list[list[int]]) -> int:
    """Part3: no limit on how many events; must handle 10^5 events well under 2 s."""
    # TODO
    return 0


def part1(lines: list[str]) -> list[str]:
    """'K <k>' / 'N <n>' / n lines 's e v' -> [best value]."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input as part1 -> [best value, 'i j ...' ascending original indices, or '-']."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'N <n>' / n lines 's e v' -> [best value]."""
    # TODO
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
