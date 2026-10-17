"""LC 199 Binary Tree Right Side View -- BFS by level, keep the last node of each level. Time O(n), space O(width)."""
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Level-order list with None holes, like LeetCode: [3,9,20,None,None,15,7]."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    for node in queue:
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def find(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)

# --- solution ---
def right_side_view(root):
    if not root:
        return []
    out = []
    queue = deque([root])
    while queue:
        out.append(queue[-1].val)                 # rightmost node of this level
        for _ in range(len(queue)):               # freeze the level size, then drain exactly that many
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return out
# --- end ---

if __name__ == "__main__":
    assert right_side_view(build_tree([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert right_side_view(build_tree([1, None, 3])) == [1, 3]
    assert right_side_view(build_tree([])) == []
    assert right_side_view(build_tree([1, 2])) == [1, 2]            # left-only deeper level is visible
    assert right_side_view(build_tree([1, 2, 3, 4])) == [1, 3, 4]
    print("ok 199_binary_tree_right_side_view")
