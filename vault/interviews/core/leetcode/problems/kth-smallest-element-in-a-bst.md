---
slug: kth-smallest-element-in-a-bst
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜Medium

给二叉搜索树的根节点 `root` 和整数 `k`，返回第 `k` 小的元素（`k` 从 `1` 开始）。

## A
**一句话。** BST 的中序遍历是升序：递归中序，数到第 `k` 个就返回。

```python
def kth_smallest(root, k):
    def inorder(node):
        nonlocal k
        if not node:
            return None
        found = inorder(node.left)
        if found is not None:
            return found
        k -= 1
        if k == 0:
            return node.val
        return inorder(node.right)
    return inorder(root)
```

**复杂度。** 时间 `O(h + k)`，空间 `O(h)`。

**易错点。**
- 入节点就计数、再去左子树：变成先序，`[5,3,6,2,4,null,null,1]`、`k = 3` 得 `2`，应为 `3`。
- 用递归写链状 BST：`10^4` 层超过 CPython 递归上限，抛 `RecursionError`。

**追问。**
- 树频繁修改且频繁查询？：每个节点维护子树大小 `size`，按左子树大小与 `k` 比较往下走，`O(h)`。
- 第 `k` 大？：镜像遍历（右、根、左），或求第 `n - k + 1` 小。

**同模式。** LC 98 验证二叉搜索树、LC 173 二叉搜索树迭代器、LC 94 二叉树的中序遍历、LC 538 把二叉搜索树转换为累加树
