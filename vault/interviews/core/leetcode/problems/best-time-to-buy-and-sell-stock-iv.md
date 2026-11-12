---
slug: best-time-to-buy-and-sell-stock-iv
---
## Q
**LC 188 买卖股票的最佳时机 IV**｜Hard

给每天价格 `prices` 和整数 `k`，最多完成 `k` 笔交易（买卖各一次，再买前须先卖），求最大利润。

## A
**一句话。** 状态机 DP：`buy[i][j]` 持有第 `j` 笔，`sell[i][j]` 空仓且最多完成 `j` 笔，逐天转移。

```python
def max_profit(k, prices):
    n = len(prices)
    # 第 0 天不可能有货，buy 初值 -inf
    buy = [[-inf] * (k + 1) for _ in range(n + 1)]
    sell = [[0] * (k + 1) for _ in range(n + 1)]
    for i, p in enumerate(prices, 1):
        for j in range(1, k + 1):
            buy[i][j] = max(buy[i-1][j], sell[i-1][j-1] - p)
            sell[i][j] = max(sell[i-1][j], buy[i-1][j] + p)
    return sell[n][k]
```

**复杂度。** 时间 `O(nk)`，空间 `O(nk)`。

**易错点。**
- `buy` 第 0 行写成 `0`：等于免费拿到股票，`(2,[3,2,6,5,0,3])` 得 `9`，应为 `7`。
- 买入从 `sell[i-1][j]` 转移：不占新笔数，`k` 的限制失效；必须用 `sell[i-1][j-1]`。
- 答案取 `buy[n][k]`：未卖出的持仓不是已实现利润。

**追问。**
- `k` 很大怎么办？：`k >= n//2` 时不再受限，累加所有正的相邻差价。
- 空间能压吗？：`i` 维可滚动，`j` 从大到小更新，压到 `O(k)`。

**同模式。** LC 121 买卖股票的最佳时机、LC 123 买卖股票的最佳时机 III、LC 309 含冷冻期、LC 714 含手续费
