"""q07 Inorder Traversal: recursive -> iterative -> Morris — reference solution.

Classic LeetCode 94 (Binary Tree Inorder Traversal), asked at Snowflake with a live follow-up:
"bonus point if you can do it in constant space" (Morris traversal). part1/part2/part3 must all
produce byte-identical output; the only thing that changes is how much extra memory / call-stack
depth each one uses:

  part1  recursive         O(h) call stack, O(1) extra heap
  part2  iterative + stack O(1) call stack, O(h) heap (explicit list-as-stack)
  part3  Morris             O(1) call stack, O(1) heap (temporary threaded links, restored)
"""
from __future__ import annotations

import sys


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: list[str]) -> TreeNode | None:
    """Build a tree from a LeetCode-style level-order list. 'null' or '' marks a missing child.

    Standard BFS build: values[0] is the root; walk a queue of "parents awaiting children" and
    consume values two at a time (left, right) for each parent, skipping null slots entirely
    (a null node contributes no further slots to consume).
    """
    values = list(values)
    if not values or values[0] in ("null", ""):
        return None
    root = TreeNode(int(values[0]))
    queue = [root]
    i = 1
    n = len(values)
    while queue and i < n:
        node = queue.pop(0)
        if i < n:
            left_val = values[i]
            i += 1
            if left_val not in ("null", ""):
                node.left = TreeNode(int(left_val))
                queue.append(node.left)
        if i < n:
            right_val = values[i]
            i += 1
            if right_val not in ("null", ""):
                node.right = TreeNode(int(right_val))
                queue.append(node.right)
    return root


def part1(root: TreeNode | None) -> list[int]:
    """Recursive inorder traversal (left, node, right). O(h) call-stack depth."""
    out: list[int] = []

    def visit(node: TreeNode | None) -> None:
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)

    visit(root)
    return out


def part2(root: TreeNode | None) -> list[int]:
    """Iterative inorder traversal using an explicit stack (a Python list on the heap, not the
    call stack) -- no recursion."""
    out: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


def part3(root: TreeNode | None) -> list[int]:
    """Morris inorder traversal: O(1) extra space, no stack, no recursion.

    For each node, if it has a left subtree, find its inorder predecessor (rightmost node of the
    left subtree) and thread predecessor.right -> node temporarily. That thread lets us return to
    `node` after finishing the left subtree without a stack. The second time we arrive at `node`
    via the thread, we remove it (restoring the tree to its original shape) before moving right.
    """
    out: list[int] = []
    node = root
    while node is not None:
        if node.left is None:
            out.append(node.val)
            node = node.right
            continue
        # find the inorder predecessor of `node`: rightmost node in node.left's subtree
        predecessor = node.left
        while predecessor.right is not None and predecessor.right is not node:
            predecessor = predecessor.right
        if predecessor.right is None:
            # first visit: thread predecessor -> node, then descend left
            predecessor.right = node
            node = node.left
        else:
            # second visit (via the thread): restore the tree, emit node, go right
            predecessor.right = None
            out.append(node.val)
            node = node.right
    return out


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
