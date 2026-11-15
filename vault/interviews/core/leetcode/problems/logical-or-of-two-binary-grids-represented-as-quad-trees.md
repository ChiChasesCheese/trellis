---
slug: logical-or-of-two-binary-grids-represented-as-quad-trees
---
## Q
**LC 558 四叉树交集**｜Medium

两个 `n x n` 的 0/1 网格各用四叉树表示（叶结点 `isLeaf` 表示整块同值，`val` 是该值；非叶结点有 `topLeft`、`topRight`、`bottomLeft`、`bottomRight`）。返回两网格按位或的四叉树。

## A
**一句话。** 任一方是叶子就能直接定论（值为 1 则整块为 1，否则结果就是另一方）；否则四块各自递归，若四个结果是同值叶子就合并成一个叶子。

```python
def intersect(a, b):
    if a.isLeaf:
        return a if a.val else b     # 全 1 吞掉一切，全 0 不起作用
    if b.isLeaf:
        return b if b.val else a
    tl = intersect(a.topLeft, b.topLeft)
    tr = intersect(a.topRight, b.topRight)
    bl = intersect(a.bottomLeft, b.bottomLeft)
    br = intersect(a.bottomRight, b.bottomRight)
    kids = (tl, tr, bl, br)
    if all(k.isLeaf and k.val == tl.val for k in kids):
        return Node(tl.val, True, None, None, None, None)
    return Node(False, False, tl, tr, bl, br)
```

**复杂度。** 时间 `O(两棵树的结点数之和)`，空间 `O(深度)`。

**易错点。**
- 四个孩子递归后不合并：四个全 1 的叶子应收缩成一个叶子，否则结果不是规范形。
- 合并时只判 `isLeaf` 不判值：四个叶子值不同时不能合并。
- 叶子 `a.val` 为 0 时返回 `a` 而不是 `b`：全 0 与任何块相或等于另一块。

**追问。**
- 返回 `a`、`b` 本身有风险吗？：结果和输入共享结点，若之后要修改输入，需要深拷贝。
- 为什么递归深度只有 `log n`？：每层把边长折半，到 `1 x 1` 必为叶子。

**同模式。** LC 427 建立四叉树、LC 100 相同的树、LC 617 合并二叉树
