---
slug: tt-spiral-matrix-constant-space
---
## Q
**螺旋矩阵（O(1) 额外空间、不改输入）**｜Medium

`m x n` 矩阵，按顺时针螺旋顺序返回所有元素。额外空间 `O(1)`，不能改输入也不能用 `visited`，要处理空矩阵、单行、单列。例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,3,6,9,8,7,4,5]`。

## A
**一句话。** 维护 `top`、`bottom`、`left`、`right` 四条边界，每圈走上、右、下、左四条边后各收一格，下边和左边要先判断还有多于一行、一列。

```python
def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # 上边
            out.append(matrix[top][c])
        for r in range(top + 1, bottom + 1):    # 右边
            out.append(matrix[r][right])
        if top < bottom:                        # 多于一行才有下边
            for c in range(right - 1, left - 1, -1):
                out.append(matrix[bottom][c])
        if left < right:                        # 多于一列才有左边
            for r in range(bottom - 1, top, -1):
                out.append(matrix[r][left])
        top, bottom = top + 1, bottom - 1
        left, right = left + 1, right - 1
    return out
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 少了 `top < bottom` 守卫：`[[1,2,3]]` 又倒着走一遍，得 `[1,2,3,2,1]`。
- 少了 `left < right` 守卫：`[[1],[2],[3]]` 得 `[1,2,3,2]`。
- 空矩阵：`[]`、`[[]]` 没有首行或首列，开头必须先判断。

**追问。**
- 螺旋矩阵 II（LC 59）？：同样的边界顺序，反过来往格子里填 `1..n^2`。
- 螺旋矩阵 III（LC 885）？：从某格向外，步长按 `1, 1, 2, 2, 3, 3...` 增长，越界的格子丢弃。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 885 螺旋矩阵 III、LC 2326 螺旋矩阵 IV
