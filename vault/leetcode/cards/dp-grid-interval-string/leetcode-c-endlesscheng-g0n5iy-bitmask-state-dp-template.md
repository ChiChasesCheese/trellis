---
id: leetcode-c-endlesscheng-g0n5iy-bitmask-state-dp-template
node: dp-grid-interval-string.bitmask-state-dp
type: cloze
anki: 1787272478480
tags: [concept-cloze, leetcode, recall, template]
---
向集合加入第 i 个对象的写法是 {{c1::mask | (1 << i)}}。

```
def min_subset_sum_cost(cost):
    n = len(cost)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        for i in range(n):
            if mask >> i & 1 == 0:
                nxt = mask | (1 << i)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[i])
    return dp[-1]
```

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.09%20-%20%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
