---
slug: construct-quad-tree
---
## Q
**LC 427 建立四叉树**｜Medium

把 `n * n` 的 0/1 矩阵表示成四叉树：区域内值全相同则是叶子，否则分成四个象限递归。

## A
**一句话。** 对区域 `(r, c, size)` 递归建四个象限，四个孩子都是同值叶子就合并成一个叶子。

```python
def construct(grid):
    def build(r, c, size):
        if size == 1:
            return Node(bool(grid[r][c]), True)
        h = size // 2
        tl = build(r, c, h)
        tr = build(r, c + h, h)
        bl = build(r + h, c, h)
        br = build(r + h, c + h, h)
        kids = (tl, tr, bl, br)
        if all(k.isLeaf for k in kids) and \
                len({k.val for k in kids}) == 1:
            return Node(tl.val, True)
        return Node(True, False, tl, tr, bl, br)
    return build(0, 0, len(grid))
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 只比较孩子的 `val`、不检查是否叶子：内部节点的 `val` 都取 `True`，会被误合并成叶子。
- 重复扫描子网格判断同值：自底向上只看四个孩子即可，不用再扫格子。

**追问。**
- 为什么递归深度不用担心？：深度只有 `log2(n) <= 6`。
- 想少建节点怎么办？：先扫一遍判断全同值再决定是否递归，是自顶向下的写法，最坏更慢。

**同模式。** LC 558 四叉树交集、LC 108 将有序数组转换为二叉搜索树、LC 105 从前序与中序遍历序列构造二叉树
