---
slug: lowest-common-ancestor-of-a-binary-tree
---
## Q
**LC 236 二叉树的最近公共祖先**｜Medium

给二叉树和其中两个节点 `p`、`q`，返回它们的最近公共祖先（节点可以是自己的祖先）。

## A
**一句话。** 后序递归：碰到 `p` 或 `q` 就返回自己，左右都有返回说明分居两侧，当前节点就是答案，否则往上传非空的一边。

```python
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root              # 碰到 p/q 立刻返回，不再深入
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root              # p、q 分居两侧
    return left or right
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 碰到 `p` 还往下找：`p=5, q=4`（`4` 在 `5` 下）会返回 `4`，应为 `5`。
- `left` 非空就提前返回，不看右边：`p=5, q=1` 返回 `5`，应为 `3`。
- 单链树深 `10^5` 会 `RecursionError`，要调大递归上限。

**追问。**
- 不递归怎么做？：遍历时记父指针，把 `p` 及其全部祖先放进集合，`q` 向上爬，第一个命中的就是答案。
- 同一棵树要回答大量查询？：预处理深度和倍增表，每次 `O(log n)`。

**同模式。** LC 235 二叉搜索树的最近公共祖先、LC 160 相交链表、LC 1650 含父指针的最近公共祖先、LC 1644 最近公共祖先 II
