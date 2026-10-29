---
id: tlc-perfect-squares-2-code
node: a.perfect-squares
type: qa
step: 2
---
## Q
**LC 279 完全平方数**｜写出 Python 实现

给 `1 <= n <= 10^4`，求和为 `n` 的完全平方数的最少个数（每个平方数可以用多次）。

## A
**思路。** `dp[i]` 表示和为 `i` 的最少平方数个数。凑成 `i` 的最后一个平方数是某个 `j²`（`j² <= i`），所以 `dp[i] = 1 + min(dp[i - j²])`；`dp[0] = 0`，`i` 从小到大填。

```python
from math import inf, isqrt


def num_squares(n: int) -> int:
    dp = [0] + [inf] * n                    # dp[i]：和为 i 的最少完全平方数个数
    for i in range(1, n + 1):
        dp[i] = 1 + min(dp[i - j * j] for j in range(1, isqrt(i) + 1))   # 枚举最后一个平方数 j²
    return dp[n]
```

运行：`12` → `3`，`13` → `2`，`1` → `1`，`7` → `4`，`10000` → `1`，`9999` → `4`。

**复杂度。** 时间 `O(n√n)`：第 `i` 轮试 `isqrt(i)` 个平方数；空间 `O(n)`。

**写法要点。** `math.isqrt` 返回精确的整数平方根，避免浮点开方的误差；`[0] + [inf] * n` 一次写好基准和「不可达」；`min` 里放生成器表达式，不建中间列表；`inf + 1` 仍是 `inf`，但这里每个 `i` 至少能用 `1` 凑出，最终都是整数。
