"""pc19 Rewrite Tree With Subtree Sums -- YOUR implementation. Run the tests against this file
with IMPL=starter.

Part1: root1/root2 are level-order arrays of a COMPLETE binary tree (children of i are
2i+1, 2i+2, same shape = same length). Return a new array, root2's shape, holding each node's
subtree sum computed from root1's VALUES.

Part2 (general tree, node objects, must be iterative -- no recursion, trees can be 1e5 deep):
same transformation on a `TreeNode` tree that may have gaps (missing children).
"""

from __future__ import annotations

import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


def rewrite_subtree_sums(root1: list[int], root2: list[int]) -> list[int]:
    """Part1. ValueError if root1 and root2 are not the same length."""
    # TODO
    return []


def rewrite_subtree_sums_tree(root1: "TreeNode | None") -> "TreeNode | None":
    """Part2: must be iterative (explicit stack), no recursion -- trees can be 1e5 deep."""
    # TODO
    return None


def _build_tree(tokens: list[str]) -> "TreeNode | None":
    """Build a tree from a LeetCode-style preorder token stream ('#' = missing child)."""
    # TODO
    return None


def _serialize_preorder(root: "TreeNode | None") -> list[str]:
    """Iterative preorder with '#' markers for missing children."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """each line: 'root1_values | root2_values' -> the rewritten array, space-separated."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """each line: a preorder token stream -> the rewritten tree's preorder token stream."""
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
