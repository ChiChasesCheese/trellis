"""pc10 Distributed Tree Count -- YOUR implementation. Run the tests against this file with
IMPL=starter.

Nodes talk only through one global FIFO channel (exactly-once, in send order). Log every delivery
as `from->to:MESSAGE`; end with `ROOT_COUNT:<n>` (Part2: `ROOT_COUNT:<n> PARTIAL` when a subtree
was given up). See problem.md for the full protocol and the drop/retry rules.
"""

from __future__ import annotations

import sys


def simulate_tree_count(parent: list[int], drops: set[int] | None = None) -> list[str]:
    """Part1 when `drops` is None/empty; Part2 when some send ids are dropped.
    Raise ValueError for an empty array, not exactly one root, an out-of-range parent, or a cycle."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """one line: space-separated parent array."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """line 1 parent array; line 2 'DROPS <id> <id> ...' (may list no ids)."""
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
