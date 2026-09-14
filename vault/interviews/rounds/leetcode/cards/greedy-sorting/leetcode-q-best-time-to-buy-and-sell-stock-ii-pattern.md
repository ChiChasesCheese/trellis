---
id: leetcode-q-best-time-to-buy-and-sell-stock-ii-pattern
node: greedy-sorting.greedy
type: qa
anki: 1787776730254
tags: [lc::122, leetcode, pattern, recall]
---
## Q
股票买卖问题（无限次交易，122题）如何用状态机 DP 建模？

## A
定义两个状态：empty_profit（今天不持股的最大利润）和 holding_profit（今天持股的最大利润）。转移：
holding_profit = max(holding_profit, empty_profit - price)
empty_profit = max(empty_profit, holding_profit + price)
初始 holding_profit = -inf, empty_profit = 0，遍历一遍 prices 即可，O(n) 时间 O(1) 空间。这套「hold/empty 两状态滚动」模板可扩展到 III/IV（加 transaction 计数维度）和 cooldown/fee（加冷冻期或手续费扣减）等变种。

**Evidence**

maxProfit2: holding_profit, empty_profit = -inf, 0; for price in prices: new_holding_profit = max(empty_profit - price, holding_profit); empty_profit = max(empty_profit, holding_profit + price); holding_profit = new_holding_profit

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F122%20-%20Best%20Time%20to%20Buy%20and%20Sell%20Stock%20II)
