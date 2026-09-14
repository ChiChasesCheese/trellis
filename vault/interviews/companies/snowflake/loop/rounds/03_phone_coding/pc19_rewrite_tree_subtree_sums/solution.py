"""pc19 Rewrite Tree With Subtree Sums -- reference solution.

Part1: two SAME-SHAPE complete binary trees given as level-order (array) lists, indices related
the usual heap way (children of i are 2i+1, 2i+2). "Write into root2 each node's subtree sum
from root1": root2's own values are irrelevant (the whole point is to overwrite them), so the
result is a pure function of root1; root2 is kept as a parameter only to check the shape (equal
length) contract the problem states, matching the two-tree framing of the one-hand preview.
Complete-tree arrays let this be done bottom-up in a single reverse pass with no recursion at
all: every child index is strictly greater than its parent's, so by the time index i is visited
(scanning from n-1 down to 0) both of its children already hold their final subtree sums.

Part2 (reconstructed): the same transformation but for a general binary tree with gaps, using
actual node objects (`TreeNode`) instead of a dense array -- a complete-tree ARRAY can't
represent a skewed tree of depth 1e5 (it would need 2**100000 slots), so the follow-up switches
representations, not just implementation. Both traversals (compute sums, rebuild) are done
ITERATIVELY with an explicit stack, so a depth-1e5 skewed tree never touches Python's recursion
limit. The line-oriented wrapper serialises/deserialises trees as a LeetCode-style preorder
token stream with '#' for a missing child, which is O(n) even for a fully skewed tree (an array
serialisation would not be).
"""

from __future__ import annotations

import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


# --------------------------------------------------------------------------- Part 1
def rewrite_subtree_sums(root1: list[int], root2: list[int]) -> list[int]:
    """root1/root2: level-order arrays of a COMPLETE binary tree (children of i are 2i+1, 2i+2).
    Returns a new array, the same shape as root2, holding each node's subtree sum computed from
    root1's values. ValueError if the two arrays are not the same length (not the same shape)."""
    if len(root1) != len(root2):
        raise ValueError("root1 and root2 must have the same shape (equal length)")
    n = len(root1)
    sums = list(root1)
    for i in range(n - 1, -1, -1):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n:
            sums[i] += sums[left]
        if right < n:
            sums[i] += sums[right]
    return sums


# --------------------------------------------------------------------------- Part 2
def _postorder_nodes(root: "TreeNode | None") -> list[TreeNode]:
    """Iterative postorder (children before parent), safe at any depth."""
    if root is None:
        return []
    order: list[TreeNode] = []
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if processed:
            order.append(node)
            continue
        stack.append((node, True))
        if node.left is not None:
            stack.append((node.left, False))
        if node.right is not None:
            stack.append((node.right, False))
    return order


def rewrite_subtree_sums_tree(root1: "TreeNode | None") -> "TreeNode | None":
    """General binary tree (arbitrary gaps / depth), node objects, iterative. Returns a NEW tree
    of the same shape as root1 holding each node's subtree sum."""
    order = _postorder_nodes(root1)  # children-before-parent
    sums: dict[TreeNode, int] = {}
    for node in order:
        total = node.val
        if node.left is not None:
            total += sums[node.left]
        if node.right is not None:
            total += sums[node.right]
        sums[node] = total

    new_of: dict[TreeNode, TreeNode] = {}
    for node in order:  # children were appended before their parent -> already in new_of
        new_node = TreeNode(sums[node])
        if node.left is not None:
            new_node.left = new_of[node.left]
        if node.right is not None:
            new_node.right = new_of[node.right]
        new_of[node] = new_node
    return new_of[root1] if root1 is not None else None


# --------------------------------------------------------------------------- (de)serialisation
def _build_tree(tokens: list[str]) -> "TreeNode | None":
    """Build a tree from a LeetCode-style preorder token stream ('#' = missing child),
    iteratively (no recursion, so a depth-1e5 skewed tree is fine)."""
    it = iter(tokens)

    def next_node() -> "TreeNode | None":
        tok = next(it)
        return None if tok == "#" else TreeNode(int(tok))

    root = next_node()
    if root is None:
        return None
    stack: list[tuple[TreeNode, int]] = [(root, 0)]  # state 0: need left, state 1: need right
    while stack:
        node, state = stack.pop()
        if state == 0:
            stack.append((node, 1))
            child = next_node()
            if child is not None:
                node.left = child
                stack.append((child, 0))
        else:
            child = next_node()
            if child is not None:
                node.right = child
                stack.append((child, 0))
    return root


def _serialize_preorder(root: "TreeNode | None") -> list[str]:
    """Iterative preorder with '#' markers for missing children."""
    tokens: list[str] = []
    stack: list[TreeNode | None] = [root]
    while stack:
        node = stack.pop()
        if node is None:
            tokens.append("#")
            continue
        tokens.append(str(node.val))
        stack.append(node.right)
        stack.append(node.left)
    return tokens


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """each line: 'root1_values | root2_values' (space-separated ints on each side) -> the
    rewritten array, space-separated."""
    out = []
    for line in lines:
        left, right = line.split("|")
        root1 = [int(x) for x in left.split()]
        root2 = [int(x) for x in right.split()]
        out.append(" ".join(map(str, rewrite_subtree_sums(root1, root2))))
    return out


def part2(lines: list[str]) -> list[str]:
    """each line: a preorder token stream ('#' for a missing child) -> the rewritten tree's
    preorder token stream."""
    out = []
    for line in lines:
        root1 = _build_tree(line.split())
        rewritten = rewrite_subtree_sums_tree(root1)
        out.append(" ".join(_serialize_preorder(rewritten)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
