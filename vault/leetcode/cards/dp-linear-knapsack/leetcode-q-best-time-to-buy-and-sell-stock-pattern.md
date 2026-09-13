---
id: leetcode-q-best-time-to-buy-and-sell-stock-pattern
node: dp-linear-knapsack.dynamic-programming
type: qa
anki: 1787776730052
tags: [lc::121, leetcode, pattern, recall]
---
## Q
「买卖股票最佳时机」(只能交易一次)有哪几种等价的解法思路？

## A
1) 一次遍历维护历史最低价 lowest_price，同时更新 max_profit = max(max_profit, p - lowest_price)；2) 状态机 DP：dp[0]=之前空仓/今天买入后的价值(=max(dp[0],-p))，dp[1]=之前持有/今天卖出后的价值(=max(dp[1],dp[0]+p))；3) Kadane 变式：对差分数组 diff[i]=prices[i]-prices[i-1] 跑最大子数组和，因为利润=某段相邻差值之和；4) 前后缀分解：pre_min[i] 表示 [0,i] 的最小价格，post_max[i] 表示 [i,n-1] 的最大价格，答案是 max(post_max[i]-pre_min[i])。四种方法本质都是 O(n) 时间、O(1)~O(n) 空间。

**Evidence**

maxProfit0(单调最低价)、maxProfit1(状态机 dp[0]/dp[1])、maxProfit2(注释:'Kadane 把问题转成最大连续子数组和，对差分数组跑 Kadane')、maxProfit(pre_min/post_max 前后缀分解)四个解法并存于 My Solution 代码块中。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F121%20-%20Best%20Time%20to%20Buy%20and%20Sell%20Stock)
