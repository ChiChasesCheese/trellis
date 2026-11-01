---
slug: lowest-common-ancestor-of-a-binary-search-tree
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Medium

给定一个二叉搜索树，找到该树中两个指定节点的最近公共祖先。最近公共祖先的定义为：对于有根树 `T` 的两个结点 `p`、`q`，最近公共祖先是一个结点 `x`，满足 `x` 是 `p`、`q` 的祖先且 `x` 的深度尽可能大（一个节点也可以是它自己的祖先）。所有节点的值都是唯一的；`p`、`q` 为不同节点且均存在于给定的二叉搜索树中。

例：`root = [6,2,8,0,4,7,9,null,null,3,5]`，`p = 2`，`q = 8` → `6`；`p = 2`，`q = 4` → `2`（节点可以是它自己的祖先）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** BST 的二分性质用于 LCA：从根往下走，第一个「把 `p`、`q` 分在两侧（或等于其一）」的结点就是答案。

**一句话。** 若 `p`、`q` 都比当前结点小就进左子树，都比它大就进右子树，否则当前结点就是最近公共祖先。

**识别。** 普通二叉树的 LCA（LC 236）要遍历整棵树；这里是 BST，值的大小关系直接告诉你 `p`、`q` 在哪一侧，只走一条路径。

**推导。** 对结点 `x`：若 `p`、`q` 都小于 `x.val`，它们都在左子树，LCA 一定在左子树里；都大于则在右子树。一旦出现 `p.val <= x.val <= q.val`（或反过来），要么两者分居两侧，要么 `x` 就是其中一个，那么更深的结点不可能同时是两者的祖先，`x` 就是答案。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if p.val < root.val and q.val < root.val:       # 两个都在左边：答案在左子树
        return lowest_common_ancestor(root.left, p, q)
    if p.val > root.val and q.val > root.val:       # 两个都在右边：答案在右子树
        return lowest_common_ancestor(root.right, p, q)
    return root                                     # 分居两侧，或 root 就是其中之一：分叉点
```

**运行。** `[6,2,8,0,4,7,9,null,null,3,5]`：`p = 2, q = 8` → `6`；`p = 2, q = 4` → `2`；`p = 3, q = 5` → `4`；`p = 0, q = 5` → `2`。

**复杂度。** 时间 `O(h)`；空间 `O(h)`（递归栈）。

**拓展优化。**
- 迭代写法：递归是尾调用，直接改成循环，空间 `O(1)`，也避开递归上限。
```python
def lowest_common_ancestor_iterative(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    while True:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```
- 普通二叉树（LC 236）：后序递归，左右子树各找一次，两侧都找到则当前结点是答案。

**易错点。**
- 把比较写成 `<=` / `>=`：例 2（`p = 2, q = 4`）走到结点 `2` 时因为 `2 >= 2` 且 `4 >= 2` 继续进右子树，最后返回 `3`，正确是 `2`。
- 直接比较结点对象 `p < root`：`TreeNode` 没有定义大小比较，抛 `TypeError`；要比较 `.val`。
- 递归深度等于树高：退化成链的 BST 超过 CPython 默认约 1000 的递归上限会 `RecursionError`，此时用迭代版。

**同模式。** LC 236 二叉树的最近公共祖先、LC 700 二叉搜索树中的搜索、LC 701 二叉搜索树中的插入操作、LC 450 删除二叉搜索树中的节点。
