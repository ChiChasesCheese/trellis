---
id: tlc-best-time-to-buy-and-sell-stock-iv-2-code
node: b.best-time-to-buy-and-sell-stock-iv
type: qa
step: 2
---
## Q
**LC 188 买卖股票的最佳时机 IV**｜写出 Python 实现

写 `max_profit(k, prices)`：最多完成 `k` 笔交易（一次买入加一次卖出），再次买入前必须先卖出，求最大利润。`1 <= k <= 100`，`1 <= len(prices) <= 1000`，`0 <= prices[i] <= 1000`。

## A
**思路。** `buy[i][j]`：第 `i` 天结束时手上有货、已经买入 `j` 笔（第 `j` 笔还没卖）的最大收益，第 0 行是 `-inf`；`sell[i][j]`：第 `i` 天结束时手上没货、最多完成 `j` 笔的最大收益，第 0 行是 `0`。逐天填表：`buy` 要么沿用昨天，要么用 `sell[i-1][j-1]` 买入；`sell` 要么沿用昨天，要么用 `buy[i-1][j]` 卖出；答案在 `sell[n][k]`。

```python
from math import inf


def max_profit(k: int, prices: list[int]) -> int:
    n = len(prices)
    # buy[i][j]：第 i 天结束时手上有货，且已经买入 j 笔（第 j 笔还没卖）的最大收益
    # sell[i][j]：第 i 天结束时手上没货，且最多完成 j 笔的最大收益
    buy = [[-inf] * (k + 1) for _ in range(n + 1)]    # 第 0 天不可能有货：-inf
    sell = [[0] * (k + 1) for _ in range(n + 1)]      # 第 0 天没做过交易：收益 0
    for i, p in enumerate(prices, 1):
        for j in range(1, k + 1):
            buy[i][j] = max(buy[i - 1][j], sell[i - 1][j - 1] - p)   # 继续拿着 / 今天开第 j 笔
            sell[i][j] = max(sell[i - 1][j], buy[i - 1][j] + p)      # 继续空仓 / 今天卖掉
    return sell[n][k]
```

运行：`(2, [2,4,1])` → `2`，`(2, [3,2,6,5,0,3])` → `7`，`(1, [3,2,6,5,0,3])` → `4`，`(3, [3,2,6,5,0,3])` → `7`，`(1, [1])` → `0`，`(100, [1,2,3,4,5])` → `4`，`(2, [7,6,4,3,1])` → `0`；`k = 100`、`n = 1000` 的随机价格不到 `0.5` 秒算完。

**复杂度。** 时间 `O(n·k)`：两张表各 `(n+1)×(k+1)` 格，每格常数；空间 `O(n·k)`。

**写法要点。**
- `[[-inf] * (k + 1) for _ in range(n + 1)]`：每行各建一个新列表，不要写成 `[[-inf] * (k + 1)] * (n + 1)`（所有行是同一个对象）。
- `-inf` 来自 `math`：比任何实际收益都小的初值，保证没买入时不会被当成合法状态；用 `float('-inf')` 等价。
- `enumerate(prices, 1)` 让 `i` 直接是天数（第几天），`p` 是当天价格，不用写 `prices[i - 1]`。
- `sell[i - 1][j - 1]` 放在 `buy[i][j]` 的转移里，`j = 1` 时读第 0 列 `sell[i-1][0] = 0`，表示「没有任何交易、利润 `0`」；下标 `0` 这一列对应「零笔」。
