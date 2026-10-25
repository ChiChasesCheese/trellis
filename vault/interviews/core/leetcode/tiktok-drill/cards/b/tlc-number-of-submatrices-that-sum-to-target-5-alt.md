---
id: tlc-number-of-submatrices-that-sum-to-target-5-alt
node: b.number-of-submatrices-that-sum-to-target
type: qa
step: 5
---
## Q
**LC 1074 元素和为目标值的子矩阵数量**｜另一种解法

不压缩成一维，直接用二维前缀和枚举所有子矩阵怎么写？它在什么规模下可以用，和行对压缩的做法怎么选？

## A
**思路。** 先建二维前缀和 `pre`，`pre[i][j]` 是左上角 `i` 行 `j` 列的元素和；任意子矩阵（行 `r1..r2-1`、列 `c1..c2-1`）的和由四个角的前缀和用容斥求出：`pre[r2][c2] - pre[r1][c2] - pre[r2][c1] + pre[r1][c1]`。枚举全部四个边界，数等于 `target` 的个数。

```python
def num_submatrix_sum_target_brute(matrix: list[list[int]], target: int) -> int:
    m, n = len(matrix), len(matrix[0])
    pre = [[0] * (n + 1) for _ in range(m + 1)]            # pre[i][j]：左上角 i 行 j 列的和
    for i in range(m):
        for j in range(n):
            pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + matrix[i][j]
    return sum(
        1
        for r1 in range(m) for r2 in range(r1 + 1, m + 1)
        for c1 in range(n) for c2 in range(c1 + 1, n + 1)
        if pre[r2][c2] - pre[r1][c2] - pre[r2][c1] + pre[r1][c1] == target
    )
```

运行：示例 1 → `4`，示例 2 → `5`，示例 3 → `0`。

**为什么对。** 子矩阵由 `r1 < r2`、`c1 < c2`（前缀和下标，半开区间）唯一确定，四重循环覆盖了每个非空子矩阵恰好一次；四角容斥公式是标准的二维区间和。

**取舍。** 暴力 `O(R^2 C^2)`：`100 × 100` 有约 `2.5 * 10^7` 个子矩阵，每个 `O(1)`，勉强可以跑；`R`、`C` 再大就不行。行对压缩 + 前缀和计数是 `O(R^2 C)`，是预期解。暴力的价值：写得快、几乎不会错，适合作为对照，先用它确认题意，再写优化版。
