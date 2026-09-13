"""q03 Tree Height Reduction -- YOUR implementation.

Three parts, three DIFFERENT sources, three DIFFERENT node-indexing / depth conventions.
Keep each part faithful to ITS OWN convention -- see problem.md.
"""
from __future__ import annotations

import sys


def part1(parent: list[int], k: int) -> list[int]:
    """nodes 1..n; parent[i] (0-indexed i) = parent of node i+2; node 1 = root, root depth 1.
    Return the sorted ids of nodes to delete so max depth <= k."""
    # TODO
    return []


def part2(parent: list[int], k: int) -> int:
    """nodes 0-indexed; parent[i] = parent of node i; parent[root] == -1; root depth 0.
    Return the minimum number of whole-subtree deletions so max depth <= k."""
    # TODO
    return 0


def part3(tree_nodes: int, tree_from: list[int], tree_to: list[int], max_operations: int) -> int:
    """nodes 1-indexed, root = 1, height in edges. tree_from[i] -> tree_to[i] are directed
    parent -> child edges. Each operation detaches a child subtree and reattaches it directly
    under the root. Return the minimum achievable height using at most max_operations ops."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """See problem.md for the exact per-part stdin/stdout layout (first line: PART <1|2|3>)."""
    # TODO
    stdout.write("\n")


if __name__ == "__main__":
    main()
