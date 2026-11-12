---
slug: lowest-common-ancestor-of-a-binary-tree-iii
---
## Q
**LC 1650 二叉树的最近公共祖先 III**｜Medium

每个节点有父指针，给二叉树中的两个节点 `p`、`q`，求它们的最近公共祖先。

## A
**一句话。** 与链表相交同理：两指针各沿父链上行，走到根就换到对方起点，总步数相同，必在 LCA 相遇。

```python
def lowest_common_ancestor(p, q):
    a, b = p, q
    while a is not b:
        a = a.parent if a.parent else q   # 到根后换起点
        b = b.parent if b.parent else p
    return a
```

**复杂度。** 时间 `O(h)`，空间 `O(1)`。

**易错点。**
- 到根不换起点、直接 `a = a.parent`：指针变成 `None`，下一步 `None.parent` 抛 `AttributeError`。
- 用 `val` 判断相遇：值可能重复，应用 `is` 比较节点身份。

**追问。**
- 没有父指针呢？：LC 236，从根递归，左右都找到则当前节点是 LCA。
- 大量查询同一棵树？：预处理倍增表，每次查询 `O(log n)`。

**同模式。** LC 160 相交链表、LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 1676 二叉树的最近公共祖先 IV
