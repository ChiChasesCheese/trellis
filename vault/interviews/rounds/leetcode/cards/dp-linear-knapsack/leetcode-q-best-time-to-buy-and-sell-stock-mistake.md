---
id: leetcode-q-best-time-to-buy-and-sell-stock-mistake
node: dp-linear-knapsack.dynamic-programming
type: qa
anki: 1787776730150
tags: [lc::121, leetcode, mistake, recall]
---
## Q
求「只交易一次的最大利润」时，为什么双重循环枚举买入卖出日 (i, j) 会 TLE？

## A
双重循环遍历所有 (i, j) 对是 O(n²)，而 n 最大可达 1e5，1e10 次操作必然超时。本质上买卖利润只依赖『当前价格 - 历史最低价』，不需要枚举所有 pair，只需一次遍历动态维护历史最低价即可把复杂度降到 O(n)（对应笔记中的 maxProfit0）。

**Evidence**

代码块中保留了 maxProfit_tle 方法：用双重 for 循环 (`for i in range(len(prices)) for j in range(i+1, len(prices))`) 枚举所有买卖组合求最大差值，方法名后缀 `_tle` 明确标注该写法会超时。

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F121%20-%20Best%20Time%20to%20Buy%20and%20Sell%20Stock)
