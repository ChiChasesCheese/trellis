---
id: tlc-best-time-to-buy-and-sell-stock-with-transaction-fee-2-code
node: a.best-time-to-buy-and-sell-stock-with-transaction-fee
type: qa
step: 2
---
## Q
**LC 714 买卖股票的最佳时机含手续费**｜写出 Python 实现

股价数组 `prices`（长度 `1` 到 `5 * 10^4`，`1 <= prices[i] < 5 * 10^4`），手续费 `fee`（`0 <= fee < 5 * 10^4`），交易次数不限、同时最多持一股、每笔付一次手续费，求最大利润。要求 `O(n)`。

## A
**思路。** 两个状态：第 `i` 天结束时不持股的最大利润 `dp[i][0]`、持股的最大利润 `dp[i][1]`。不持股来自「昨天不持股」或「昨天持股今天卖出并付费」，持股来自「昨天持股」或「昨天不持股今天买入」。

```python
def max_profit(prices: list[int], fee: int) -> int:
    n = len(prices)
    # dp[i][0]: 第 i 天结束时手里没股票的最大利润；dp[i][1]: 手里有股票的最大利润
    dp = [[0, 0] for _ in range(n)]
    dp[0][1] = -prices[0]                      # 第 0 天只能买入或什么都不做
    for i in range(1, n):
        # 不持有 = 昨天就没有，或昨天持有、今天卖出（卖出时付手续费）
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i] - fee)
        # 持有 = 昨天就持有，或昨天没有、今天买入
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
    return dp[-1][0]                           # 最后一天不持股一定不比持股差
```

运行：`[1,3,2,8,4,9], 2` → `8`，`[1,3,7,5,10,3], 3` → `6`，`[5], 0` → `0`，`[5,4,3], 1` → `0`，`[1,2], 3` → `0`。

**复杂度。** 时间 `O(n)`：每天两次 `max`；空间 `O(n)`：`n` 行 2 列的表。

**写法要点。** `[[0, 0] for _ in range(n)]` 每行是独立的列表，`[[0, 0]] * n` 会让所有行指向同一个对象；`dp[-1][0]` 用负下标取最后一行；状态含义写在注释里，转移方程一行一个状态，面试官能逐行对照。
