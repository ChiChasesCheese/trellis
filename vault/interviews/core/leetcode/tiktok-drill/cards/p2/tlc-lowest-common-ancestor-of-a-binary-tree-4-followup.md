---
id: tlc-lowest-common-ancestor-of-a-binary-tree-4-followup
node: p2.lowest-common-ancestor-of-a-binary-tree
type: qa
step: 4
---
## Q
**LC 236 二叉树的最近公共祖先**｜追问

面试官接着问：（1）有没有不建父指针的写法？它在什么输入上会出问题？（2）同一棵树要回答 `10^5` 次不同的 `(p, q)` 查询怎么办？（3）如果 `p`、`q` 不保证在树中呢？

## A
1. **递归后序**：`dfs(node)` 返回「以 `node` 为根的子树里，找到了 `p` 或 `q` 中的哪一个，或它们的最近公共祖先」。`node` 为空或就是 `p`、`q` 时直接返回 `node`；左右子树各递归一次，两边都非空说明 `p`、`q` 分居两侧，当前节点就是答案；否则返回非空的那一边。代码约 5 行，只用 `O(h)` 栈空间，但递归深度等于树高，`10^5` 层的单链树会抛 `RecursionError`。
2. **多次查询**：一次遍历预处理每个节点的深度和倍增表 `up[k][v]`（`v` 的第 `2^k` 个祖先）。查询时先把较深的节点提升到同一深度，再从大到小尝试同时上跳，预处理 `O(n log n)`，每次查询 `O(log n)`。查询离线给出时，也可以用 Tarjan 离线算法（并查集）。
3. **不保证存在**（LC 1644）：递归版里 `p`、`q` 的「找到」要单独计数，遍历结束后只有两个都找到才返回结果，否则返回 `None`。

```python
def lca_rec(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root
    left, right = lca_rec(root.left, p, q), lca_rec(root.right, p, q)
    return root if left and right else left or right
```

**Python 提醒**：`left or right` 返回第一个为真的对象本身（不是布尔值），所以能直接把找到的节点往上传；但节点对象恰好都为真，如果节点类重写了 `__len__` 或 `__bool__`，这个写法会出错。
