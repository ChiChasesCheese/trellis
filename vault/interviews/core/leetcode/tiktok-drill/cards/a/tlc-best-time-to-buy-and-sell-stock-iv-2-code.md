---
id: tlc-best-time-to-buy-and-sell-stock-iv-2-code
node: a.best-time-to-buy-and-sell-stock-iv
type: qa
step: 2
---
## Q
**LC 188 买卖股票的最佳时机 IV**｜写出 Python 实现

写 `max_profit(k, prices)`：最多完成 `k` 笔交易（一次买入加一次卖出），再次买入前必须先卖出，求最大利润。`1 <= k <= 100`，`1 <= len(prices) <= 1000`，`0 <= prices[i] <= 1000`。

## A
**思路。** `buy[j]`：完成 `j-1` 笔后、第 `j` 笔已买入未卖时的最大收益（初值 `-inf`）；`sell[j]`：最多完成 `j` 笔交易时的最大收益（初值 `0`）。每天对每个 `j` 依次更新 `buy[j]`、`sell[j]`；`k >= n // 2` 时改用累加所有正价差。

```python
from itertools import pairwise
from math import inf


def max_profit(k: int, prices: list[int]) -> int:
    if k >= len(prices) // 2:                    # 交易次数不受限：只要上涨就赚，所有正的相邻差之和
        return sum(max(b - a, 0) for a, b in pairwise(prices))
    buy = [-inf] * (k + 1)                       # buy[j]：完成 j-1 笔后，第 j 笔已买入未卖时的最大收益
    sell = [0] * (k + 1)                         # sell[j]：最多完成 j 笔交易的最大收益
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
```

运行：`(2, [2,4,1])` → `2`，`(2, [3,2,6,5,0,3])` → `7`，`(1, [3,2,6,5,0,3])` → `4`，`(3, [3,2,6,5,0,3])` → `7`，`(1, [1])` → `0`，`(100, [1,2,3,4,5])` → `4`，`(2, [7,6,4,3,1])` → `0`。

**复杂度。** 时间 `O(n·min(k, n // 2))`，空间 `O(k)`。

**写法要点。**
- `itertools.pairwise(prices)`（3.10+）直接给出相邻价格对 `(prices[i], prices[i+1])`，比 `zip(prices, prices[1:])` 少一份拷贝，也不用下标。
- `-inf` 来自 `math`：比任何实际收益都小的初值，保证没买入时不会被当成合法状态；用 `float('-inf')` 等价。
- `sell[j - 1]` 放在 `buy[j]` 的转移里，`j = 1` 时用 `sell[0] = 0` 表示“没有任何交易、利润 `0`”；`sell` 和 `buy` 长度都是 `k + 1`，下标 `0` 对应“零笔”。
- `max(b - a, 0)` 放在生成器里直接 `sum`，累加所有上涨的差价，不需要显式找谷和峰。
