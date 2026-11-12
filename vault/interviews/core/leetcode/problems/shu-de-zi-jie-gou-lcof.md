---
slug: shu-de-zi-jie-gou-lcof
---
## Q
**剑指 Offer 26 树的子结构**｜Medium

判断 `tree2` 是否是 `tree1` 的子结构：`tree1` 中存在某节点，以它为根向下能与 `tree2` 的每个节点对上（不要求到叶子）。空树不是任何树的子结构。

## A
**一句话。** 外层递归枚举 `tree1` 的每个节点当候选根，内层 `match` 同步向下比对。

```python
def is_sub_structure(tree1, tree2):
    def match(a, b):
        if b is None:                # b 这支到头了，a 多的不管
            return True
        if a is None or a.val != b.val:
            return False
        return (match(a.left, b.left)
                and match(a.right, b.right))

    if tree1 is None or tree2 is None:
        return False                 # 空树不算子结构
    return (match(tree1, tree2)
            or is_sub_structure(tree1.left, tree2)
            or is_sub_structure(tree1.right, tree2))
```

**复杂度。** 时间 `O(mn)`，空间 `O(h1 + h2)`。

**易错点。**
- 当成「子树」（LC 572）：要求 `a` 那块与 `b` 完全相同，`[3,6,7,1,8]` 与 `[6,1]` 会得 `False`，应为 `True`。
- `match` 先判 `a` 为空再判 `b` 为空：`b` 为空时无论 `a` 如何都应成功。
- 漏掉空树判断：`tree2` 为空应返回 `False`。

**追问。**
- LC 572 怎么改？：`match` 要求两边同时为空或值相等，其余不变。
- 想要 `O(m + n)`？：先序序列化（空节点占位）后做子串匹配，仅适用于 LC 572。

**同模式。** LC 572 另一棵树的子树、LC 100 相同的树、LC 101 对称二叉树、LC 226 翻转二叉树
