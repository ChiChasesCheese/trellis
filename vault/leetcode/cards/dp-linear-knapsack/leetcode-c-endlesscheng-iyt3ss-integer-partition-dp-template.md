---
id: leetcode-c-endlesscheng-iyt3ss-integer-partition-dp-template
node: dp-linear-knapsack.integer-partition-dp
type: cloze
anki: 1787272429804
tags: [concept-cloze, leetcode, recall, template]
---
无序拆分计数的内层 total 应从 part {{c1::递增}}。

```
def partition_count(n, mod):
    dp = [0] * (n + 1)
    dp[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            dp[total] = (dp[total] + dp[total - part]) % mod
    return dp[n]
```

**Evidence**

§7.2 整数拆分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.17%20-%20%E6%95%B4%E6%95%B0%E6%8B%86%E5%88%86%E8%AE%A1%E6%95%B0)
