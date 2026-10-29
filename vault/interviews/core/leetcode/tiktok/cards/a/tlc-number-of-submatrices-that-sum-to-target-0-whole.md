---
id: tlc-number-of-submatrices-that-sum-to-target-0-whole
node: a.number-of-submatrices-that-sum-to-target
type: qa
---
## Q
**LC 1074 元素和为目标值的子矩阵数量**｜Hard · 字节 高频

给一个矩阵 `matrix` 和目标值 `target`，返回元素总和等于 `target` 的**非空子矩阵**的数量。子矩阵由 `(x1, y1, x2, y2)` 决定，包含所有满足 `x1 <= x <= x2`、`y1 <= y <= y2` 的单元 `matrix[x][y]`；只要有一个坐标不同就算不同的子矩阵。`1 <= matrix.length, matrix[0].length <= 100`，`-1000 <= matrix[i][j] <= 1000`，`-10^8 <= target <= 10^8`。例：`matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0` → `4`（四个只含 `0` 的 `1x1` 子矩阵）；`matrix = [[1,-1],[-1,1]], target = 0` → `5`；`matrix = [[904]], target = 0` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 枚举上下两条边界 `(top, bottom)`，把这几行按列求和压成一维数组 `col`；问题变成「一维数组里和为 `target` 的子数组有多少个」，用前缀和加哈希计数在 `O(C)` 内数完；总时间 `O(R^2 · C)`。

**识别。** 「数子矩阵个数、和等于目标」是二维前缀和的信号。元素有负数，滑动窗口失效。常用降维：固定上下边界后，每一列变成一个数，左右边界的选择就是 LC 560（和为 `K` 的子数组）。`100 × 100`：`O(R^2 · C) = 10^6` 很轻松，`O(R^2 C^2)` 约 `2.5 * 10^7` 个子矩阵也能过，但不是预期解。

**推导。** 暴力：枚举两个角，求和，`O(R^3 C^3)`；用二维前缀和 `O(1)` 求和，降到 `O(R^2 C^2)`。浪费在于：上下边界固定后，左右边界的枚举其实是一个一维计数问题。一维：设前缀和为 `s_j`，以第 `j` 列结尾、和为 `target` 的子数组个数，等于之前出现过多少次前缀和 `s_j - target`——用哈希表记录每个前缀和出现的次数，一次扫描完成。`bottom` 下移一行，只要把新行加进 `col`。

```python
from collections import Counter


def num_submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    m, n = len(matrix), len(matrix[0])
    ans = 0
    for top in range(m):
        col = [0] * n                      # col[c]：第 top..bottom 行、第 c 列的和
        for bottom in range(top, m):
            col = [a + b for a, b in zip(col, matrix[bottom])]
            seen = Counter({0: 1})         # 前缀和 -> 出现次数；空前缀和为 0
            s = 0
            for v in col:                  # 把 col 当一维数组：数和为 target 的子数组
                s += v
                ans += seen[s - target]    # 以当前列结尾、前缀和为 s - target 的起点个数
                seen[s] += 1
    return ans
```

运行：示例 1 → `4`，示例 2 → `5`，示例 3 → `0`，`[[5]]`、`target = 5` → `1`。

**复杂度。** 时间 `O(R^2 · C)`；空间 `O(C)`（`col` 与哈希表）。

**易错点。**
- 哈希表必须以 `{0: 1}` 开头（空前缀）：否则从第一列开始的子数组被漏掉，`[[5]]`、`target = 5` 得到 `0`（正确 `1`），`[[1,-1],[-1,1]]`、`target = 0` 得到 `1`（正确 `5`）。
- 先查询再更新：`ans += seen[s - target]` 要在 `seen[s] += 1` **之前**。反过来写，`target = 0` 时当前前缀会数到自己（空子数组）：`[[904]]`、`target = 0` 得到 `1`（正确 `0`）。
- 滑动窗口（双指针）不能用：有负数，`s > target` 时缩左端会错过解。`[[1,-1],[-1,1]]`、`target = 0` 得到 `4`（正确 `5`）。

**追问。**
- `R` 远大于 `C` 时先转置，使枚举的行对数更少，变成 `O(min^2 · max)`。
- 和**不超过** `target` 的子矩阵个数：哈希计数失效，改用有序结构（`bisect`）维护前缀和，`O(R^2 C log C)`。
- 要列出每个子矩阵的坐标：哈希表的值改成起点下标列表，命中时展开。

**同模式。** LC 560 和为 K 的子数组、LC 363 矩形区域不超过 K 的最大数值和、面试题 17.24 最大子矩阵、LC 974 和可被 K 整除的子数组、LC 525 连续数组。
