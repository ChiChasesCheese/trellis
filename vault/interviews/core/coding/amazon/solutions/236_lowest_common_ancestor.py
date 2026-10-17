"""LC 236 Lowest Common Ancestor of a Binary Tree -- postorder DFS: return the node if it is p, q, or the split point."""
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
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root                                  # found a target (or fell off the tree)
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:                               # p and q are in different subtrees -> root splits them
        return root
    return left or right                             # both targets are on one side (or absent)
# --- end ---

if __name__ == "__main__":
    t = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    n = lambda v: find(t, v)
    assert lowest_common_ancestor(t, n(5), n(1)).val == 3
    assert lowest_common_ancestor(t, n(5), n(4)).val == 5          # a node is its own ancestor
    assert lowest_common_ancestor(t, n(6), n(4)).val == 5
    assert lowest_common_ancestor(t, n(7), n(8)).val == 3
    one = build_tree([1, 2])
    assert lowest_common_ancestor(one, one, one.left).val == 1
    print("ok 236_lowest_common_ancestor")
