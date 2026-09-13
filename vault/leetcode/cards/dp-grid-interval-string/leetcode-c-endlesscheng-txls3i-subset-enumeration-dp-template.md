---
id: leetcode-c-endlesscheng-txls3i-subset-enumeration-dp-template
node: dp-grid-interval-string.subset-enumeration-dp
type: cloze
anki: 1787272415405
tags: [concept-cloze, leetcode, recall, template]
---
SOS 子集和核心更新是 dp[mask] += {{c1::dp[mask ^ (1 << bit)]}}。

```
def solve(values, width):
    size = 1 << width
    dp = values[:]
    for bit in range(width):
        for mask in range(size):
            if mask & (1 << bit):
                dp[mask] += dp[mask ^ (1 << bit)]
    return dp
```

**Evidence**

§9.6 SOS DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.13%20-%20%E5%AD%90%E9%9B%86%E6%9E%9A%E4%B8%BE%E4%B8%8E%20SOS%20DP)
