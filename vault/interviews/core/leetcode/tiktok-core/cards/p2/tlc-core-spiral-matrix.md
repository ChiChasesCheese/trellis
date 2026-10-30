---
id: tlc-core-spiral-matrix
node: p2.spiral-matrix
type: qa
---
## Q
**LC 54 螺旋矩阵**｜Medium · LC TikTok 热度 75/100（近 3 个月） · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 139 次 · 最近 2026-10-14（CodeTop） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给一个 `m` 行 `n` 列的矩阵 `matrix`，按**顺时针螺旋顺序**返回矩阵中的所有元素。`m == matrix.length`，`n == matrix[i].length`，`1 <= m, n <= 10`，`-100 <= matrix[i][j] <= 100`。例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,3,6,9,8,7,4,5]`；`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1,2,3,4,8,12,11,10,9,5,6,7]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 维护四个边界 `top / bottom / left / right`，每一圈依次沿上边（左到右）、右边（上到下）、下边（右到左）、左边（下到上）取元素，取完一圈四个边界各向内收一格；单行、单列的情形要防止下边和左边重复取。`O(mn)`。

**识别。** 「按固定的路径遍历矩阵」是模拟题，考的是边界处理，不涉及算法技巧。`m, n <= 10`，任何线性写法都足够，关键是单行 / 单列 / 一个元素这些退化情形不重复、不遗漏。

**推导。** 两种常见做法：方向向量加访问标记（走到边界或已访问就右转），或者收缩边界。边界法不需要 `visited` 数组：一圈的四条边按固定顺序取，每取完一条就知道它对应的边界要收。退化情形的出现是因为第三、四步（下边、左边）取的行或列可能已经被第一、二步取过：当只剩一行（`top == bottom`）或一列（`left == right`）时，必须跳过这两步。

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

**复杂度。** 时间 `O(mn)`，每个元素恰好取一次；空间 `O(1)` 额外（不计输出）。

**易错点。**
- 漏掉 `top < bottom and left < right` 的保护，单行或单列会被重复读取：`[[1,2,3]]` 得到 `[1,2,3,2,1]`，`[[1],[2],[3]]` 得到 `[1,2,3,2]`。
- 下边是 `matrix[bottom][left:right]` 的**反向**，不包含最右一格（它已在右边取过）；左边的行范围是 `bottom - 1` 到 `top + 1`，不包含两端。
- 切片 `matrix[top + 1 : bottom + 1]` 的结束下标要加一才包含 `bottom` 行。

**追问。**
- 生成螺旋矩阵（LC 59）：反过来按螺旋顺序填入 `1..n^2`，用方向向量加"撞墙右转"。
- 用 `zip` 的短写法：取走第一行，把剩余矩阵逆时针转 90 度，循环到空；写起来短，但每轮都重建矩阵，是 `O(mn * min(m, n))`。
- 逆时针螺旋或从内向外的螺旋：改变四条边的顺序，或把结果反转。

**同模式。** LC 59 螺旋矩阵 II、LC 885 螺旋矩阵 III、LC 48 旋转图像、LC 73 矩阵置零、LC 498 对角线遍历。
