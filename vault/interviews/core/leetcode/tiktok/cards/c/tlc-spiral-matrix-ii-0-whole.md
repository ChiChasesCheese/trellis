---
id: tlc-spiral-matrix-ii-0-whole
node: c.spiral-matrix-ii
type: qa
---
## Q
**LC 59 螺旋矩阵 II**｜Medium · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 16 次 · 最近 2024-08-21（国内 CodeTop）

给定正整数 `n`，生成一个包含 `1` 到 `n^2` 所有元素、按顺时针螺旋顺序排列的 `n x n` 正方形矩阵。`1 <= n <= 20`。例：`n = 3` → `[[1,2,3],[8,9,4],[7,6,5]]`；`n = 1` → `[[1]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按「右、下、左、上」的方向循环依次填 `1..n^2`，下一格越界或已填就顺时针转向。

**识别。** 「螺旋遍历 / 按方向走」：方向向量加「撞墙转向」比手写四条边的边界收缩更不容易错，同样的写法能处理非方阵（LC 54）。

**推导。** 手写 `top / bottom / left / right` 四个边界逐圈填，每圈四个循环，奇数 `n` 时中心点的收尾容易出错。用一个方向向量 `(dr, dc)` 沿当前方向走；下一格出界或已经填过（矩阵里还是 `0`）就转向。顺时针转向的向量变换是 `(dr, dc) -> (dc, -dr)`：`(0,1) -> (1,0) -> (0,-1) -> (-1,0) -> (0,1)`。

```python
def generate_matrix(n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]         # 0 表示还没填
    r = c = 0
    dr, dc = 0, 1                                # 初始方向：向右
    for value in range(1, n * n + 1):
        matrix[r][c] = value
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n and matrix[nr][nc] == 0):
            dr, dc = dc, -dr                     # 撞墙或撞到已填的格子：顺时针转 90 度
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return matrix
```

运行：`n = 3` → `[[1,2,3],[8,9,4],[7,6,5]]`，`n = 1` → `[[1]]`，`n = 4` → `[[1,2,3,4],[12,13,14,5],[11,16,15,6],[10,9,8,7]]`。

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`（不计输出）。

**拓展优化。**
- 逐圈边界收缩写法不用 `0` 标记，也不用转向，适合要求 `O(1)` 额外状态的场合：

```python
def generate_matrix_layers(n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    value = 1
    while top <= bottom and left <= right:       # 每圈填四条边，然后四个边界各收一格
        for c in range(left, right + 1):
            matrix[top][c] = value; value += 1
        for r in range(top + 1, bottom + 1):
            matrix[r][right] = value; value += 1
        for c in range(right - 1, left - 1, -1):
            matrix[bottom][c] = value; value += 1
        for r in range(bottom - 1, top, -1):
            matrix[r][left] = value; value += 1
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return matrix
```

- 非方阵（LC 54 读出矩阵）要给最后一圈加 `top < bottom and left < right` 的判断，否则单行或单列会被重复填写。

**易错点。**
- 转向后忘了重新计算下一格：转向后 `nr, nc` 仍是旧方向的越界位置，下一轮写入越界。
- 方向变换写成 `(dr, dc) -> (-dc, dr)`：那是逆时针，第一次撞墙后变成向上，下一格越界。
- 边界法四条边的 `range` 端点没有错开：角点被两条边各写一次，`value` 多走，矩阵里会出现大于 `n^2` 的数。

**追问。**
- 螺旋遍历读出矩阵（LC 54）：同样的方向向量，访问并标记，非方阵也适用。
- 逆时针或从中心向外螺旋：改初始方向和转向规则，或把顺时针结果的值倒过来。

**同模式。** LC 54 螺旋矩阵、LC 885 螺旋矩阵 III、LC 48 旋转图像、LC 498 对角线遍历、LC 2326 螺旋矩阵 IV。
