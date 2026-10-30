---
id: tlc-cheapest-flights-within-k-stops-2-code
node: p4.cheapest-flights-within-k-stops
type: qa
step: 2
---
## Q
**LC 787 K 站中转内最便宜的航班**｜写出 Python 实现

`n` 个城市（`2 <= n <= 100`），航班列表 `flights`（`[from, to, price]`，价格 `1` 到 `10^4`，无重复、无自环，至多 `n * (n - 1) / 2` 条），出发地 `src`、目的地 `dst`（`src != dst`）和 `k`（`0 <= k < n`）。返回最多中转 `k` 次的最低价格，没有这样的路线返回 `-1`。

## A
**思路。** `dp[t][v]` 是最多坐 `t` 趟航班、从 `src` 到城市 `v` 的最小价格。第 0 行只有 `dp[0][src] = 0`，其余无穷。第 `t` 行先复制第 `t - 1` 行（少坐一趟也算），再对每条航班 `u → v` 用上一行的 `dp[t-1][u] + w` 更新 `dp[t][v]`。填完 `k + 1` 行，答案是 `dp[k+1][dst]`。

```python
from math import inf


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    # dp[t][v]：最多坐 t 趟航班，从 src 到城市 v 的最小价格
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0                          # 0 趟航班：只在出发地，价格 0
    for t in range(1, k + 2):               # 最多 k 个中转 = 最多 k + 1 趟航班
        dp[t] = dp[t - 1][:]                # 少坐一趟也算（"最多 t 趟"）
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:  # 只读上一行：这一行多坐的恰好一趟
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

运行：示例 1（`k = 1`）→ `700`，示例 2（`k = 1`）→ `200`，示例 3（`k = 0`）→ `500`，`n = 3`、`flights = [[0,1,5]]`、`src = 0`、`dst = 2`、`k = 2` → `-1`。

**复杂度。** 时间 `O(k * E)`：`k + 1` 行，每行扫描全部航班；空间 `O(k * n)`：`(k + 2) × n` 的表。

**写法要点。**
- `from math import inf`，用 `inf` 表示不可达；`dp[t-1][u] + w` 在 `dp[t-1][u]` 是 `inf` 时仍是 `inf`，比较自然为假，不需要额外判断。
- `dp[t - 1][:]` 复制整行，`O(n)`；第 `t` 行以此为起点，就表达了「最多 `t` 趟」而不是「恰好 `t` 趟」。
- `for u, v, w in flights` 把航班三元组直接解包。
- 类型标注 `list[list[float]]`，因为 `inf` 是浮点数；返回时对有限值转成 `int`。
- 不需要邻接表：Bellman-Ford 遍历边列表即可。
