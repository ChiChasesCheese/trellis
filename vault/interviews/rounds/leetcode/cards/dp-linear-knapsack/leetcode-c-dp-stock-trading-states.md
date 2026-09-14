---
id: leetcode-c-dp-stock-trading-states
node: dp-linear-knapsack.dp-stock-trading-states
type: cloze
anki: 1787102264010
tags: [concept-cloze, leetcode, recall]
---
在股票交易的多状态DP中，hold（持有股票）状态应初始化为 {{c1::负无穷（-inf）}}，以避免出现「没有买入就卖出」的非法转移路径；而未持有状态初始化为 {{c2::0}}。

转移方程：dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])（持有）；dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])（不持有）。若hold初始化为0而非-inf，会让算法误以为第0天可以凭空持有股票。

**Evidence**

Pitfalls: hold和not_hold初始化反了或遗漏；Python Tricks: 初始化hold为-inf，避免没买就卖的假方案

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E8%82%A1%E7%A5%A8%E4%BA%A4%E6%98%93%E5%A4%9A%E7%8A%B6%E6%80%81%20DP)
