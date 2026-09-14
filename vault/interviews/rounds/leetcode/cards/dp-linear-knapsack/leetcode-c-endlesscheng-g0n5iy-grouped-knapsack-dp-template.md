---
id: leetcode-c-endlesscheng-g0n5iy-grouped-knapsack-dp-template
node: dp-linear-knapsack.grouped-knapsack-dp
type: cloze
anki: 1787272478779
tags: [concept-cloze, leetcode, recall, template]
---
分组背包避免重复选同组方案的直接办法是先复制 {{c1::old = dp[:]}}。

```
def grouped_knapsack(groups, capacity):
    dp = [0] * (capacity + 1)
    for group in groups:
        old = dp[:]
        for used, value in group:
            for cap in range(used, capacity + 1):
                dp[cap] = max(dp[cap], old[cap - used] + value)
    return max(dp)
```

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.10%20-%20%E5%88%86%E7%BB%84%E8%83%8C%E5%8C%85)
