---
id: tlc-patterns-tree-dfs-4-lca
node: patterns.tree-dfs
type: qa
step: 4
---
## Q
**二叉树 DFS（Tree DFS）｜最近公共祖先（LC 236）的三种情况**

不用父指针，怎样用一次后序递归找到两个节点的最近公共祖先？递归函数返回什么，三种情况各是什么？

## A
递归函数 `lca(root, p, q)` 的含义：**在 `root` 子树里找 `p` 或 `q`**，返回找到的节点（或它们的公共祖先），没找到返回 `None`。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root                        # 找到目标，或到底了
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root                        # p、q 分居两侧：root 就是 LCA
    return left or right                   # 都在一侧（或只找到一个）：向上传递
```

建树 `[3,5,1,6,2,0,8,null,null,7,4]`：`p=5, q=1` → `3`；`p=5, q=4` → `5`（节点本身是自己的祖先）；树 `[1,2]`，`p=1, q=2` → `1`。

三种情况：
1. **`p`、`q` 在 `root` 的左右两侧** → 两边都返回非空，`root` 是答案。
2. **都在同一侧** → 另一侧返回 `None`，把那一侧的结果继续向上传。
3. **`root` 本身是 `p`（或 `q`）** → 直接返回 `root`；如果另一个在它的子树里，它就是答案；这解释了为什么遇到目标时不再向下找。

- 时间 `O(n)`，空间 `O(h)`。
- 前提：`p`、`q` 都在树里，并且节点值可重复时要用 `is` 比较节点，而不是比较值。
- 变形：BST 的 LCA（LC 235）可以利用有序性，从根向下一条路走到分叉点，`O(h)`。
- 想要多次查询 → 预处理父指针 + 深度，或倍增（Binary Lifting）。
