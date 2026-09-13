---
id: leetcode-q-best-time-to-buy-and-sell-stock-with-transaction-fee-pattern
node: greedy-sorting.greedy
type: qa
anki: 1787700071519
tags: [lc::714, leetcode, pattern, recall]
---
## Q
买卖股票问题(含手续费,不限交易次数)如何用状态机DP建模?

## A
定义 dfs(i, hold) 表示第i天、是否持仓时的最大利润。转移:
- 持仓时: max(dfs(i+1, True), dfs(i+1, False) + prices[i] - fee) # 继续持有 or 卖出(此时扣手续费)
- 空仓时: max(dfs(i+1, True) - prices[i], dfs(i+1, False)) # 买入 or 继续空仓
关键点:手续费只需在卖出(状态从hold->不hold)时扣一次,买入不扣。

**Evidence**

```
def dfs(i, hold):
    if hold:
        return max(dfs(i+1, True), dfs(i+1, False) + prices[i] - fee)
    return max(dfs(i+1, True) - prices[i], dfs(i+1, False))
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F714%20-%20Best%20Time%20to%20Buy%20and%20Sell%20Stock%20with%20Transaction%20Fee)
