"""LC 124 Binary Tree Maximum Path Sum -- postorder DFS returning the best DOWNWARD gain; a global tracks the bent path."""
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
def max_path_sum(root):
    best = float("-inf")

    def gain(node):                                   # best path that starts at node and goes down one side
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)                # a negative branch is better dropped
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)     # path that BENDS at node (may use both sides)
        return node.val + max(left, right)            # what we may hand to the parent: one side only

    gain(root)
    return best
# --- end ---

if __name__ == "__main__":
    assert max_path_sum(build_tree([1, 2, 3])) == 6
    assert max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert max_path_sum(build_tree([-3])) == -3                    # all negative: must take one node
    assert max_path_sum(build_tree([2, -1])) == 2
    assert max_path_sum(build_tree([-2, -1])) == -1
    assert max_path_sum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])) == 48
    print("ok 124_binary_tree_maximum_path_sum")
