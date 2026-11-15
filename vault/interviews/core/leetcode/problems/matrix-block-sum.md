---
slug: matrix-block-sum
---
## Q
**LC 1314 矩阵区域和**｜Medium

`m × n` 矩阵 `mat` 和整数 `k`，返回矩阵 `answer`：`answer[i][j]` 是所有满足 `i-k ≤ r ≤ i+k`、`j-k ≤ c ≤ j+k` 且在矩阵内的 `mat[r][c]` 之和。

## A
**一句话。** 二维前缀和：每个格子的答案是一个被边界夹住的矩形，用四个角的容斥 `O(1)` 求出。

```python
def matrix_block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    s = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            s[i + 1][j + 1] = (s[i][j + 1] + s[i + 1][j]
                               - s[i][j] + mat[i][j])
    ans = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            r1, c1 = max(i - k, 0), max(j - k, 0)   # 夹到边界内
            r2, c2 = min(i + k + 1, m), min(j + k + 1, n)
            ans[i][j] = (s[r2][c2] - s[r1][c2]
                         - s[r2][c1] + s[r1][c1])
    return ans
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 前缀和下标差一：`s` 多一圈 0，右下角用 `i + k + 1`（开区间）。
- 边界不夹：`i - k` 为负、`i + k` 越界时，必须用 `max`、`min` 夹回矩阵内。
- 逐格暴力求和：每格 `O(k²)`，总共 `O(mnk²)`，数据大会超时。

**追问。**
- 容斥公式怎么记？：大块 − 上方 − 左方 + 重复减掉的左上角。
- 只有一维怎么做？：一维前缀和 `s[r] - s[l]`。

**同模式。** LC 304 二维区域和检索 - 矩阵不可变、LC 1292 元素和小于等于阈值的正方形的最大边长、LC 560 和为 K 的子数组
