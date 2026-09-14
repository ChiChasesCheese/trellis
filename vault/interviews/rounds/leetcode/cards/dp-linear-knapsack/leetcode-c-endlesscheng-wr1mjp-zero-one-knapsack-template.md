---
id: leetcode-c-endlesscheng-wr1mjp-zero-one-knapsack-template
node: dp-linear-knapsack.zero-one-knapsack
type: cloze
anki: 1787272472481
tags: [concept-cloze, leetcode, recall, template]
---
0/1 背包转移为 {{c1::dp[cap] = max(dp[cap], dp[cap - weight] + value)}}。

```
def max_value_01_knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - weight] + value)
    return dp[capacity]
```

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.10%20-%200-1%20%E8%83%8C%E5%8C%85)
