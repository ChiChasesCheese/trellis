---
slug: search-in-a-binary-search-tree
---
## Q
**LC 700 二叉搜索树中的搜索**｜Easy

给二叉搜索树的根结点 `root` 和整数 `val`，返回结点值等于 `val` 的子树，不存在返回 `None`。

## A
**一句话。** 利用 BST 左小右大，每步比较后只进一边，丢掉另一半。

```python
def search_bst(root, val):
    if not root or root.val == val:
        return root              # 空了就是没有
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)
```

**复杂度。** 时间 `O(h)`，空间 `O(h)`（递归栈，改成循环是 `O(1)`）。

**易错点。**
- 两边都递归：BST 只需进一边，否则退化成 `O(n)` 的普通树搜索。
- 忘了 `not root` 的判断：值不存在时会访问 `None.val`。

**追问。**
- 怎样改成 `O(1)` 空间？：用 `while root and root.val != val` 循环，向左或向右走。
- 树退化成链怎么办？：`h` 变 `n`；换成平衡树（红黑树、AVL）保证 `h = O(log n)`。

**同模式。** LC 701 二叉搜索树中的插入操作、LC 450 删除二叉搜索树中的节点、LC 235 二叉搜索树的最近公共祖先
