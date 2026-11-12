---
slug: count-good-nodes-in-binary-tree
---
## Q
**LC 1448 统计二叉树中好节点的数目**｜Medium

好节点：从根到它的路径上没有节点的值比它大。返回二叉树中好节点的数目。

## A
**一句话。** DFS 沿路径带下当前最大值 `mx`，`node.val >= mx` 就是好节点。

```python
def good_nodes(root):
    def dfs(node, mx):         # mx：根到父节点路径上的最大值
        if not node:
            return 0
        good = node.val >= mx  # 相等也算好节点
        mx = max(mx, node.val)
        return (good + dfs(node.left, mx)
                + dfs(node.right, mx))

    return dfs(root, root.val)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 用 `>` 代替 `>=`：`[3,3,null,4,2]` 得 `2`，应为 `3`。
- 初值取 `0`：节点值可为负，`[-1]` 得 `0`，应为 `1`。

**追问。**
- 返回好节点的列表？：`good` 为真时把 `node` 加进外层列表。
- 改成「路径上没有比它小的」？：把 `max` 换成 `min`，比较方向反过来。

**同模式。** LC 98 验证二叉搜索树、LC 112 路径总和、LC 1026 节点与其祖先之间的最大差值
