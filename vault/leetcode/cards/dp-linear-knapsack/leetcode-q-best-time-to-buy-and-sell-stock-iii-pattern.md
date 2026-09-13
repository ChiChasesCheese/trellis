---
id: leetcode-q-best-time-to-buy-and-sell-stock-iii-pattern
node: dp-linear-knapsack.dynamic-programming
type: qa
anki: 1787776730355
tags: [lc::123, leetcode, pattern, recall]
---
## Q
买卖股票系列（最多 k 笔交易）的状态机 DP 如何定义状态？

## A
定义 dfs(i, hold, token)：i 为当前天数，hold 表示是否持有股票，token 表示剩余可买入次数（即剩余交易次数）。转移：
- 若 hold=True：max(继续持有 dfs(i+1,True,token), 今天卖出 dfs(i+1,False,token)+prices[i])
- 若 hold=False：max(今天买入（消耗一次token）dfs(i+1,True,token-1)-prices[i]（若token>0）, 继续空仓 dfs(i+1,False,token))
初始调用 dfs(0, False, k)，k=2 即为本题（最多两笔交易）。用 @cache 记忆化即可，也可去掉递归改为二维/三维滚动数组降低空间。

**Evidence**

```
@cache
def dfs(i: int, hold: bool, token: int) -> int:
    if i == n:
        return 0
    if hold:
        return max(
            dfs(i + 1, True, token),
            dfs(i + 1, False, token) + prices[i]
        )
    return max(
        dfs(i + 1, True, token - 1) - prices[i] if token > 0 else 0,
        dfs(i + 1, False, token)
    )
return dfs(0, False, 2)
```

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F123%20-%20Best%20Time%20to%20Buy%20and%20Sell%20Stock%20III)
