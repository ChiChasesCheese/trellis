---
id: leetcode-c-endlesscheng-v2rxsn-knapsack-dp-template
node: dp-linear-knapsack.knapsack-dp
type: cloze
anki: 1787272465281
tags: [concept-cloze, leetcode, recall, template]
---
0-1 背包转移为 dp[c] = max(dp[c], {{c1::dp[c-weight] + value}})。

```
def knapsack_01(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            dp[c] = max(dp[c], dp[c - weight] + value)
    return dp[capacity]
```

**Evidence**

二、动态规划：0-1背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.09%20-%20%E8%83%8C%E5%8C%85%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
