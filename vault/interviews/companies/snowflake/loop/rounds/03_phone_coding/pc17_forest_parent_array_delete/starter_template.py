"""pc17 Forest Parent Array Delete Node -- YOUR implementation. Run the tests against this file
with IMPL=starter.

A forest of n nodes is `parent: list[int]` of length n; `parent[i] == i` means i is a root.
Deleting a node must return a compacted, valid parent array of length n-1 (or shorter for
Part2/Part3): indices are renumbered with no gaps once the deleted node(s) are gone.
"""

from __future__ import annotations

import sys


def delete_node_children_become_roots(parent: list[int], delete_index: int) -> list[int]:
    """Part1: remove delete_index; its direct children become roots. ValueError if out of
    range."""
    # TODO
    return []


def delete_subtree(parent: list[int], delete_index: int) -> list[int]:
    """Part2: remove delete_index and its entire subtree. ValueError if out of range."""
    # TODO
    return []


def delete_nodes_batch(parent: list[int], delete_indices: list[int]) -> list[int]:
    """Part3: delete all of delete_indices simultaneously. Each survivor's new parent is its
    nearest still-alive ancestor in the ORIGINAL tree; a survivor with no live ancestor becomes
    a root. ValueError on out-of-range or duplicate indices."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """each line: 'p0 p1 ... p(n-1) | delete_index' -> resulting parent array, space-separated."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """each line: 'p0 p1 ... p(n-1) | d0 d1 ...'."""
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
