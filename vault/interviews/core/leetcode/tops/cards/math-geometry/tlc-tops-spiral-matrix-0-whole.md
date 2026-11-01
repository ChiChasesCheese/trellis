---
id: tlc-tops-spiral-matrix-0-whole
node: math-geometry.spiral-matrix
type: qa
---
## Q
**LC 54 螺旋矩阵**｜Medium · 全公司热度第 26 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你一个 `m` 行 `n` 列的矩阵 `matrix`，请按照**顺时针螺旋顺序**，返回矩阵中的所有元素。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 10`，`-100 <= matrix[i][j] <= 100`。例：`matrix = [[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,3,6,9,8,7,4,5]`；`matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1,2,3,4,8,12,11,10,9,5,6,7]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 矩阵遍历模拟：四个边界逐圈收缩。

**一句话。** 维护 `top, bottom, left, right` 四个边界，每圈按「上边向右、右边向下、下边向左、左边向上」走一遍，然后四个边界各向内收一格。

**识别。** 「按固定路径遍历矩阵」是模拟题：难点不在算法，在于边界条件，尤其是只剩一行或一列时不能重复走。`m, n <= 10`，`O(mn)`。

**推导。** 方向向量加访问标记也能做（见拓展优化），要额外 `O(mn)` 空间。用四个边界不需要标记数组：每圈走完，最外一圈就被「删掉」。圈的最后阶段要防重复：下边和左边只在剩下**至少两行两列**时才存在，否则它们和上边、右边是同一批格子。

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    res: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):           # 上边：左 -> 右
            res.append(matrix[top][j])
        for i in range(top + 1, bottom + 1):       # 右边：上 -> 下（跳过已走的右上角）
            res.append(matrix[i][right])
        if top < bottom and left < right:          # 还剩至少两行两列，下边和左边才不会重复
            for j in range(right - 1, left - 1, -1):   # 下边：右 -> 左（跳过右下角）
                res.append(matrix[bottom][j])
            for i in range(bottom - 1, top, -1):       # 左边：下 -> 上（跳过两个角）
                res.append(matrix[i][left])
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return res
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1, 2, 3, 6, 9, 8, 7, 4, 5]`；`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]`；`[[1,2,3]]` → `[1, 2, 3]`；`[[1],[2],[3]]` → `[1, 2, 3]`；`[[1,2],[3,4],[5,6]]` → `[1, 2, 4, 6, 5, 3]`。

**复杂度。** 时间 `O(mn)`，每个元素恰好取一次；空间 `O(1)` 额外（不计输出）。

**拓展优化。**
- 方向向量加访问标记，没有边界特判，逻辑最直观：撞墙或走过就右转。
```python
def spiral_order_dirs(matrix: list[list[int]]) -> list[int]:
    m, n = len(matrix), len(matrix[0])
    seen = [[False] * n for _ in range(m)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]      # 右、下、左、上：顺时针
    r = c = d = 0
    res: list[int] = []
    for _ in range(m * n):                         # 每格恰好走一次
        res.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
            d = (d + 1) % 4                        # 撞墙或走过：右转
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return res
```

**易错点。**
- 漏掉 `top < bottom and left < right` 的保护：单行 `[[1,2,3]]` 下边再走一遍，得 `[1, 2, 3, 2, 1]`；单列 `[[1],[2],[3]]` 左边再走一遍，得 `[1, 2, 3, 2]`。
- 圈内起点终点重复：右边应从 `top + 1` 开始、下边应从 `right - 1` 开始，否则四个角被数两次。
- 循环条件写成 `top < bottom and left < right`：只剩一行或一列时整圈被跳过。`[[1,2,3]]` 得 `[]`，正确是 `[1, 2, 3]`。

**同模式。** LC 59 螺旋矩阵 II、LC 48 旋转图像、LC 885 螺旋矩阵 III、LC 498 对角线遍历。
