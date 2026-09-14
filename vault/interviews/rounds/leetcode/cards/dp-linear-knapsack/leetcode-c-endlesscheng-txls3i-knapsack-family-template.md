---
id: leetcode-c-endlesscheng-txls3i-knapsack-family-template
node: dp-linear-knapsack.knapsack-family
type: cloze
anki: 1787272413003
tags: [concept-cloze, leetcode, recall, template]
---
完全背包与 0-1 背包的关键循环差异是容量按 {{c1::正序}} 更新。

```
def solve(items, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for c in range(capacity, weight - 1, -1):
            dp[c] = max(dp[c], dp[c - weight] + value)
    return dp[capacity]
```

**Evidence**

§3.2 完全背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.05%20-%20%E8%83%8C%E5%8C%85%EF%BC%9A0-1%E3%80%81%E5%AE%8C%E5%85%A8%E3%80%81%E5%A4%9A%E9%87%8D%E4%B8%8E%E5%88%86%E7%BB%84)
