---
id: tlc-tt-spiral-matrix-constant-space-2-code
node: p4.tt-spiral-matrix-constant-space
type: qa
step: 2
---
## Q
**螺旋矩阵（O(1) 额外空间、不改输入）**｜写出 Python 实现

给 `m x n` 整数矩阵（`0 <= m, n <= 1000`），返回顺时针螺旋顺序的所有元素。除返回的列表外只能用 `O(1)` 额外空间，不能修改输入；要处理空矩阵、单行、单列。

## A
**思路。** 四个整数 `top, bottom, left, right` 表示还没走的矩形。每圈依次走上边、右边、（若多于一行）下边、（若多于一列）左边，然后四条边界各收一格，直到矩形为空。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out: list[int] = []                                     # 输出本身不计入额外空间
    while top <= bottom and left <= right:
        out.extend(matrix[top][c] for c in range(left, right + 1))             # 上边：左 -> 右
        out.extend(matrix[r][right] for r in range(top + 1, bottom + 1))       # 右边：上 -> 下
        if top < bottom:                                                       # 多于一行才有下边
            out.extend(matrix[bottom][c] for c in range(right - 1, left - 1, -1))
        if left < right:                                                       # 多于一列才有左边
            out.extend(matrix[r][left] for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1    # 四条边界各收一格
    return out
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1, 2, 3, 6, 9, 8, 7, 4, 5]`；`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]`；`[[1,2,3]]` → `[1, 2, 3]`；`[[1],[2],[3]]` → `[1, 2, 3]`；`[]` → `[]`；`[[]]` → `[]`；`[[1,2],[3,4]]` → `[1, 2, 4, 3]`。

**复杂度。** 时间 `O(mn)`，每个元素恰好被追加一次；额外空间 `O(1)`。

**写法要点。** 四个边界用一次元组赋值同时更新；`extend` 配生成器表达式，逐个取元素而不构造临时列表，才算真正的 `O(1)` 额外空间（`matrix[top][left:right + 1]` 这样的切片会临时分配 `O(n)`）；`range(right - 1, left - 1, -1)` 写成显式的 `range`，而不是反向切片，因为 `left = 0` 时 `left - 1` 是 `-1`，切片 `[right - 1:-1:-1]` 会被当成「从末尾倒数」而得到空列表；下边和左边的 `if` 守卫是单行单列正确性的关键。
