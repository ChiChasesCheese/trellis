---
id: leetcode-c-endlesscheng-luu0kb-knapsack-dp-template
node: dp-linear-knapsack.knapsack-dp
type: cloze
anki: 1787272457780
tags: [concept-cloze, leetcode, recall, template]
---
0-1 背包的转移骨架是 dp[c] = max(dp[c], dp[c-w] + {{c1::v}})。

```
def zero_one_knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for current in range(capacity, weight - 1, -1):
            dp[current] = max(dp[current], dp[current - weight] + value)
    return dp[capacity]
```

**Evidence**

二、动态规划：0-1 背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.07%20-%20%E8%83%8C%E5%8C%85%20DP)
