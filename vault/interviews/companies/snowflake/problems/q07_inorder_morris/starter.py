"""q07 Inorder Traversal: recursive -> iterative -> Morris — YOUR implementation.
Run: python drill.py test q07"""
from __future__ import annotations

import sys


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: list[str]) -> TreeNode | None:
    """Build a tree from a LeetCode-style level-order list. 'null' or '' marks a missing child."""
    # TODO
    return None


def part1(root: TreeNode | None) -> list[int]:
    """Recursive inorder traversal (left, node, right)."""
    # TODO
    return []


def part2(root: TreeNode | None) -> list[int]:
    """Iterative inorder traversal using an explicit stack -- no recursion."""
    # TODO
    return []


def part3(root: TreeNode | None) -> list[int]:
    """Morris inorder traversal: O(1) extra space, no stack, no recursion. Must restore the tree
    to its original shape (no dangling threads) after traversal."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format: first line 'PART n' (n in {1,2,3}); second line is a CSV level-order tree
    (LeetCode style, 'null' for missing children); an empty/absent second line means an empty
    tree. Output: one comma-joined line of the inorder values (an empty line for an empty tree)."""
    lines = stdin.read().split("\n")
    if not lines or lines[0].strip() == "":
        stdout.write("")
        return
    first = lines[0].strip()
    if not first.upper().startswith("PART"):
        raise ValueError("first line must be 'PART n'")
    part = int(first.split()[1])
    payload = lines[1].strip() if len(lines) > 1 else ""
    values = [v.strip() for v in payload.split(",")] if payload else []
    root = build_tree(values)
    fn = {1: part1, 2: part2, 3: part3}.get(part)
    if fn is None:
        raise ValueError(f"unknown part {part}")
    result = fn(root)
    stdout.write(",".join(str(v) for v in result) + "\n")


if __name__ == "__main__":
    main()
