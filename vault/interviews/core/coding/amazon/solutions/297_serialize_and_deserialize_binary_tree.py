"""LC 297 Serialize and Deserialize Binary Tree -- preorder with null markers. Time O(n), space O(n)."""
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
def serialize(root):
    out = []

    def walk(node):
        if not node:
            out.append("#")                   # explicit null marker makes the shape unambiguous
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(data):
    tokens = iter(data.split(","))

    def build():
        tok = next(tokens)                    # consume in the same preorder we wrote
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node

    return build()
# --- end ---

def _same(a, b):
    if not a or not b:
        return a is b
    return a.val == b.val and _same(a.left, b.left) and _same(a.right, b.right)

if __name__ == "__main__":
    for vals in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2, None, 3], [-1, -2, None, -3]):
        t = build_tree(vals)
        s = serialize(t)
        assert _same(deserialize(s), t), vals
    assert serialize(build_tree([1, 2, 3, None, None, 4, 5])) == "1,2,#,#,3,4,#,#,5,#,#"
    assert serialize(None) == "#"
    print("ok 297_serialize_and_deserialize_binary_tree")
