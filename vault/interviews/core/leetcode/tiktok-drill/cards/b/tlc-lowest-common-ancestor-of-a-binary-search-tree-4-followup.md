---
id: tlc-lowest-common-ancestor-of-a-binary-search-tree-4-followup
node: b.lowest-common-ancestor-of-a-binary-search-tree
type: qa
step: 4
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Easy · 字节高频｜追问

面试官接着问：（1）如果不是 BST，只是普通二叉树？（2）`p`、`q` 可能不在树里？（3）要回答大量次查询？

## A
1. **普通二叉树（LC 236）**：值没有顺序，只能遍历。后序递归：
```python
def lca_binary_tree(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)
    return root if left and right else left or right
```
`O(n)` 时间；递归深度等于树高，链状树在 Python 里会触到 1000 层上限，需要改成迭代（父指针 + 集合）。
2. **目标可能不存在**：BST 里各自从根二分一次，`O(h)` 验证存在，再求 LCA。普通树则要让递归同时统计找到了几个目标。
3. **大量查询**：BST 每次 `O(h)`；普通树用倍增（binary lifting）预处理 `O(n log n)`，每次查询 `O(log n)`，或者欧拉序加区间最小值查询（RMQ）。

**Python 提醒**：比较结点要用 `is`，不要用 `==`；`left or right` 依赖结点对象为真值，所以只能用于「没有定义 `__bool__` / `__len__` 的结点类」。
