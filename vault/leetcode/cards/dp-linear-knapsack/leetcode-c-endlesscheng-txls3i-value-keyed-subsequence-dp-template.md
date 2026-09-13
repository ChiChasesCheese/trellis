---
id: leetcode-c-endlesscheng-txls3i-value-keyed-subsequence-dp-template
node: dp-linear-knapsack.value-keyed-subsequence-dp
type: cloze
anki: 1787272414504
tags: [concept-cloze, leetcode, recall, template]
---
值域稀疏或很大时，用 {{c1::dict}} 存按值 DP。

```
def solve(nums, diff):
    best = {}
    for x in nums:
        best[x] = best.get(x - diff, 0) + 1
    return max(best.values(), default=0)
```

**Evidence**

§7.4 合法子序列 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.10%20-%20%E6%8C%89%E5%80%BC%E7%BB%93%E5%B0%BE%E7%9A%84%E5%90%88%E6%B3%95%E5%AD%90%E5%BA%8F%E5%88%97%20DP)
