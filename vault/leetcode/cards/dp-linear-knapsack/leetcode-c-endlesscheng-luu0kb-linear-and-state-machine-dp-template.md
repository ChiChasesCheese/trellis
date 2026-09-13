---
id: leetcode-c-endlesscheng-luu0kb-linear-and-state-machine-dp-template
node: dp-linear-knapsack.linear-and-state-machine-dp
type: cloze
anki: 1787272457480
tags: [concept-cloze, leetcode, recall, template]
---
滚动状态 DP 更新时，先计算 new 状态再整体赋值，避免 {{c1::同轮覆盖旧值}}。

```
def max_non_adjacent_sum(nums):
    skip = 0
    take = 0
    for value in nums:
        new_take = skip + value
        new_skip = max(skip, take)
        take, skip = new_take, new_skip
    return max(take, skip)
```

**Evidence**

二、动态规划：线性 DP、状态机 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.06%20-%20%E7%BA%BF%E6%80%A7%20DP%20%E4%B8%8E%E7%8A%B6%E6%80%81%E6%9C%BA%20DP)
