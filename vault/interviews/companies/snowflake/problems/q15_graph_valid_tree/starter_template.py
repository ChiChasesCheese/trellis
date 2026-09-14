"""q15 Graph Valid Tree -- YOUR implementation. Run the tests against this file with IMPL=starter."""

from __future__ import annotations

import sys


def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """Part1: LC261. n nodes 0..n-1, undirected edges -> True iff they form a valid tree
    (connected and acyclic). ValueError for malformed n/edges (out-of-range endpoint,
    self-loop, non-int)."""
    # TODO
    return False


def valid_tree_online(n: int, edges: list[list[int]]) -> list[tuple[bool, int]]:
    """Part2: edges arrive one at a time; for each, report (still_acyclic,
    components_remaining) after adding it."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'n m' / m lines 'u v' -> ['true' / 'false']."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """same input -> one line per edge: 'true|false components'."""
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
