---
id: tlc-unique-paths-2-code
node: b.unique-paths
type: qa
step: 2
---
## Q
**LC 62 不同路径**｜写出 Python 实现

`m x n` 网格（`1 <= m, n <= 100`），机器人从左上角出发，每次只能向下或向右一步，走到右下角。返回不同路径的条数（答案不超过 `2 * 10^9`）。给出 DP 写法，并给出等价的组合数写法。

## A
**思路。** `row` 表示当前行各格的路径数，第一行全是 `1`。下一行的每个值等于它上方的值（上一行同列）加上左边的值（本行前一列），即上一行的前缀和，所以每行 `row = list(accumulate(row))`。走完 `m - 1` 行后，右下角是 `row[-1]`。组合写法：一共 `m + n - 2` 步，选出 `m - 1` 步向下。

```python
from itertools import accumulate
from math import comb


def unique_paths(m: int, n: int) -> int:
    row = [1] * n                                # 第一行：每格只有 1 条路（一路向右）
    for _ in range(m - 1):
        row = list(accumulate(row))              # 新一行 = 上一行的前缀和：dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return row[-1]


def unique_paths_comb(m: int, n: int) -> int:
    return comb(m + n - 2, m - 1)                # 一共走 m+n-2 步，选出 m-1 步向下
```

**运行。** `(3, 7)` → `28`；`(3, 2)` → `3`；`(7, 3)` → `28`；`(3, 3)` → `6`；`(1, 1)` → `1`；`(1, 100)` → `1`；`(51, 9)` → `1916797311`。

**复杂度。** `unique_paths`：时间 `O(mn)`，空间 `O(n)`；`unique_paths_comb`：`O(min(m, n))` 次大整数运算，空间 `O(1)`。

**写法要点。** `accumulate(row)` 默认求前缀和，一行代码完成"左边的值加上方的值"；每轮用新列表替换旧列表，不会读到同一行刚更新的值；`math.comb(n, k)` 是精确的二项式系数（Python 3.8+），比自己写阶乘更短也不会溢出；两个函数的结果可以互相验证。
