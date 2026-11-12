---
slug: diameter-of-binary-tree
---
## Q
**LC 543 二叉树的直径**｜Easy

求二叉树中任意两节点之间最长路径的边数（不一定过根）。

## A
**一句话。** 后序遍历：以每个节点为最高点的最长路径是 `左高 + 右高`，全树取最大。

```python
def diameter_of_binary_tree(root):
    best = 0

    def height(node):          # 按节点数，空树为 0
        nonlocal best
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        best = max(best, lh + rh)    # 过 node 的路径边数
        return 1 + max(lh, rh)

    height(root)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 写成 `lh + rh + 1`：直径是边数，`[1,2,3,4,5]` 得 `4`，应为 `3`。
- 只算过根的路径：`5→3→2→4→6` 不经过根，只算根会漏掉。
- 链状树深度 `10^4` 会 `RecursionError`，要调大递归上限或改迭代后序。

**追问。**
- 深链不想递归？：迭代后序，栈里放 `(节点, 是否已处理孩子)`，高度存字典。
- 求最大路径和（LC 124）？：同一结构，把高度换成这一侧的最大收益 `max(0, …)`。

**同模式。** LC 124 二叉树中的最大路径和、LC 104 二叉树的最大深度、LC 687 最长同值路径、LC 110 平衡二叉树
