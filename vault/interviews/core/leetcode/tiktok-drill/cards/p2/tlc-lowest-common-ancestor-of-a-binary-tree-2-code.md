---
id: tlc-lowest-common-ancestor-of-a-binary-tree-2-code
node: p2.lowest-common-ancestor-of-a-binary-tree
type: qa
step: 2
---
## Q
**LC 236 二叉树的最近公共祖先**｜写出 Python 实现

二叉树根节点 `root`，节点数 `[2, 10^5]`，节点值互不相同，`p != q` 且都在树中。返回 `p`、`q` 的最近公共祖先节点（节点可以是自己的祖先）。

## A
**思路。** 后序递归：`lowest_common_ancestor(root, p, q)` 返回「`root` 这棵子树里找到的结果」。碰到 `None`、`p` 或 `q` 就返回它自己；左右子树各递归一次，两边都非空说明 `p`、`q` 分居两侧，当前节点就是答案，否则把非空的一边往上传。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:       # 空树、或碰到 p / q：这棵子树的汇报就是它自己
        return root
    left = lowest_common_ancestor(root.left, p, q)   # 左子树里找到了谁
    right = lowest_common_ancestor(root.right, p, q) # 右子树里找到了谁
    if left and right:                               # p、q 分居两侧：当前节点就是最近公共祖先
        return root
    return left or right                             # 只有一边有：把它往上传
```

运行：`[3,5,1,6,2,0,8,null,null,7,4]` 中 `p = 5, q = 1` → `3`，`p = 5, q = 4` → `5`；`[1,2]` 中 `p = 1, q = 2` → `1`。

**复杂度。** 时间 `O(n)`：每个节点只访问一次；空间 `O(h)`：递归栈深度等于树高，平衡树 `O(log n)`，单链树 `O(n)`。

**写法要点。** 用 `is` 比较节点对象，不比 `val`；`root is p or root is q` 放在 `root is None` 同一个守卫里，碰到就返回，不再往下找；`left or right` 返回第一个为真的节点本身（不是布尔值），一行完成「谁非空传谁」；返回类型写 `TreeNode | None`，因为子树里可能什么也没找到。单链树超过约 `1000` 层会 `RecursionError`，不递归的写法见追问卡。
