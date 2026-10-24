---
id: tlc-spiral-matrix-2-code
node: a.spiral-matrix
type: qa
step: 2
---
## Q
**LC 54 螺旋矩阵**｜写出 Python 实现

`matrix` 是 `m x n` 的整数矩阵，`1 <= m, n <= 10`，元素在 `-100` 到 `100` 之间。返回按顺时针螺旋顺序遍历得到的所有元素。

## A
**思路。** 四个边界 `top / bottom / left / right`。每圈先取上边（整行切片）和右边（逐行取最后一列）；只有剩下至少两行两列时才取下边（反向）和左边，避免重复；最后四个边界各向内收一格，直到边界交叉。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    result: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        result.extend(matrix[top][left : right + 1])                       # 上边：左 -> 右
        result.extend(row[right] for row in matrix[top + 1 : bottom + 1])  # 右边：上 -> 下
        if top < bottom and left < right:          # 还剩至少两行两列，下边和左边才不会重复走
            result.extend(reversed(matrix[bottom][left:right]))            # 下边：右 -> 左
            result.extend(matrix[r][left] for r in range(bottom - 1, top, -1))  # 左边：下 -> 上
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return result
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,3,6,9,8,7,4,5]`；`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1,2,3,4,8,12,11,10,9,5,6,7]`；`[[1]]` → `[1]`；`[[1,2,3]]` → `[1,2,3]`；`[[1],[2],[3]]` → `[1,2,3]`；`[[1,2],[3,4],[5,6]]` → `[1,2,4,6,5,3]`。

**复杂度。** 时间 `O(mn)`；空间 `O(1)` 额外。

**写法要点。** `result.extend(切片)` 和 `extend(生成器)` 一次追加多个元素，比循环 `append` 简洁；`reversed(...)` 返回迭代器，`extend` 直接消费，不建临时列表；`range(bottom - 1, top, -1)` 的两端都排除了已被上、下边取过的角；四个边界用一条元组赋值同时更新，不会出现用旧值算新值的顺序错误。
