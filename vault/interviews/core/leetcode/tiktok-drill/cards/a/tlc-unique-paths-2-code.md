---
id: tlc-unique-paths-2-code
node: a.unique-paths
type: qa
step: 2
---
## Q
**LC 62 不同路径**｜写出 Python 实现

`m x n` 网格（`1 <= m, n <= 100`），机器人从左上角出发，每次只能向下或向右一步，走到右下角。返回不同路径的条数（答案不超过 `2 * 10^9`）。给出 DP 写法，并给出等价的组合数写法。

## A
**思路。** `dp[i][j]` 表示从左上角走到 `(i, j)` 的路径数，整张表先填 `1`：第一行、第一列每格只有 `1` 条路。其余格子，最后一步从上方来（`dp[i-1][j]`）或从左边来（`dp[i][j-1]`），两者相加。答案是右下角 `dp[m-1][n-1]`。组合写法：一共 `m + n - 2` 步，选出 `m - 1` 步向下。

```python
from math import comb


def unique_paths(m: int, n: int) -> int:
    # dp[i][j]：从左上角走到 (i, j) 的路径数
    dp = [[1] * n for _ in range(m)]                 # 第一行、第一列都只有 1 条路
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]   # 最后一步从上来，或从左来
    return dp[m - 1][n - 1]


def unique_paths_comb(m: int, n: int) -> int:
    return comb(m + n - 2, m - 1)                    # 一共走 m+n-2 步，选出 m-1 步向下
```

**运行。** `(3, 7)` → `28`；`(3, 2)` → `3`；`(7, 3)` → `28`；`(3, 3)` → `6`；`(1, 1)` → `1`；`(1, 100)` → `1`；`(51, 9)` → `1916797311`。

**复杂度。** `unique_paths`：时间 `O(mn)`，空间 `O(mn)`；`unique_paths_comb`：`O(min(m, n))` 次大整数运算，空间 `O(1)`。

**写法要点。** `[[1] * n for _ in range(m)]` 一步建出带边界的表（每行是新列表，写成 `[[1] * n] * m` 所有行是同一个对象）；主循环从 `(1, 1)` 开始，`dp[i - 1][j]`、`dp[i][j - 1]` 不会越界；`math.comb(n, k)` 是精确的二项式系数（Python 3.8+），比自己写阶乘更短也不会溢出；两个函数的结果可以互相验证。
