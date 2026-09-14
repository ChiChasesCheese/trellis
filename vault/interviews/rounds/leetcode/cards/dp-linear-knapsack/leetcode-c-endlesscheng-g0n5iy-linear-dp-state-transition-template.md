---
id: leetcode-c-endlesscheng-g0n5iy-linear-dp-state-transition-template
node: dp-linear-knapsack.linear-dp-state-transition
type: cloze
anki: 1787272478180
tags: [concept-cloze, leetcode, recall, template]
---
只依赖前两项的 DP 可用 {{c1::prev2, prev1}} 滚动保存状态。

```
def max_non_adjacent(nums):
    prev2 = 0
    prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.08%20-%20%E7%BA%BF%E6%80%A7%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
