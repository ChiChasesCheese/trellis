---
slug: construct-quad-tree
---
## Q
**LC 427 建立四叉树**｜Medium

给你一个 `n * n` 的 0/1 矩阵 `grid`，用四叉树表示它并返回根节点。四叉树的每个节点有 `val`（叶子节点代表的区域的值，1 对应 True；`isLeaf` 为 False 时 `val` 取 True 或 False 都被接受）、`isLeaf`（是否叶子）和四个子节点 `topLeft`、`topRight`、`bottomLeft`、`bottomRight`。构建规则：如果当前网格的值全部相同，设 `isLeaf = True`、`val` 为该值、四个子节点为空并停止；否则 `isLeaf = False`，把网格划分成四个相等的子网格，对每个子网格递归。`n == grid.length == grid[i].length`，`n == 2^x`，`0 <= x <= 6`。例：`grid = [[0,1],[1,0]]` → 根不是叶子，四个孩子分别是值为 `0`、`1`、`1`、`0` 的叶子，序列化为 `[[0,1],[1,0],[1,1],[1,1],[1,0]]`（每项是 `[isLeaf, val]`）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 分治（divide and conquer）+ 后序合并；树的递归构造。

**一句话。** 对区域 `(r, c, size)` 递归构造四个象限，如果四个孩子都是叶子且值相同，就把它们合并成一个叶子，否则作为内部节点返回。

**识别。** 「把二维区域按四个象限递归划分」是对 `n = 2^x` 的分治；边长每次减半，递归深度只有 `x <= 6`。

**推导。** 直接照题面：在每个区域先扫描整块检查是否同值，同值就建叶子，否则划分成四块递归；每一层共扫描 `n^2` 个格子，共 `x` 层，`O(n^2 log n)`。浪费在于上层重复扫描了下层已经检查过的格子。反过来先建孩子再合并：叶子（`size = 1`）一定同值；一个区域同值当且仅当四个象限都是同值叶子且值相同，只需看孩子，`O(1)` 合并，总共 `O(n^2)`。

节点定义（LeetCode 已提供，列出便于对照）：

```python
class Node:
    def __init__(self, val: bool = False, isLeaf: bool = False,
                 topLeft: "Node | None" = None, topRight: "Node | None" = None,
                 bottomLeft: "Node | None" = None, bottomRight: "Node | None" = None) -> None:
        self.val, self.isLeaf = val, isLeaf
        self.topLeft, self.topRight = topLeft, topRight
        self.bottomLeft, self.bottomRight = bottomLeft, bottomRight
```

**简单解法。** 照题面，每块先整体扫描判断是否同值：

```python
def construct_scan(grid: list[list[int]]) -> Node | None:
    def build(r: int, c: int, size: int) -> Node:
        v = grid[r][c]
        if all(grid[i][j] == v for i in range(r, r + size) for j in range(c, c + size)):
            return Node(bool(v), True)         # 整块同值：叶子
        half = size // 2
        return Node(True, False,
                    build(r, c, half), build(r, c + half, half),
                    build(r + half, c, half), build(r + half, c + half, half))
    return build(0, 0, len(grid))
```

`O(n^2 log n)`，`n <= 64` 时完全够用。

最优解：

```python
def construct(grid: list[list[int]]) -> Node | None:
    def build(r: int, c: int, size: int) -> Node:      # 左上角 (r, c)、边长 size 的区域
        if size == 1:
            return Node(bool(grid[r][c]), True)        # 单个格子一定同值：叶子
        half = size // 2
        tl = build(r, c, half)
        tr = build(r, c + half, half)
        bl = build(r + half, c, half)
        br = build(r + half, c + half, half)
        # 同值当且仅当四个孩子都是叶子、值也一样；只看孩子，不用再扫格子
        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf and tl.val == tr.val == bl.val == br.val:
            return Node(tl.val, True)
        return Node(True, False, tl, tr, bl, br)       # 内部节点的 val 取什么都被接受
    return build(0, 0, len(grid))
```

运行：示例一序列化为 `[[0, 1], [1, 0], [1, 1], [1, 1], [1, 0]]`；全 `1` 的 `2 * 2` 网格得到单个叶子 `[[1, 1]]`；`[[0]]` 得到 `[[1, 0]]`；`8 * 8` 示例二序列化为 `[[0, 1], [1, 1], [0, 1], [1, 1], [1, 0], None, None, None, None, [1, 0], [1, 0], [1, 1], [1, 1]]`。

**复杂度。** 时间 `O(n^2)`（递推 `T(n) = 4T(n/2) + O(1)`），空间 `O(n^2)` 的节点加 `O(log n)` 的递归栈。

**易错点。**
- 只比较孩子的 `val` 而不检查它们是不是叶子：四个象限都是内部节点（内部节点 `val` 都取 `True`）时会被误合并成一个叶子，一个每个象限都混有 `0` 和 `1` 的 `4 * 4` 网格就会被错误地压成单个叶子。
- 最坏递归深度只有 `log2(n) <= 6`，远低于 CPython 默认的约 1000 层上限，不必改成迭代。

**同模式。** LC 558 四叉树交集、LC 105 从前序与中序遍历序列构造二叉树、LC 108 将有序数组转换为二叉搜索树、LC 654 最大二叉树。
