---
id: leetcode-c-endlesscheng-txls3i-take-or-skip-linear-dp-template
node: dp-linear-knapsack.take-or-skip-linear-dp
type: cloze
anki: 1787272412103
tags: [concept-cloze, leetcode, recall, template]
---
两步依赖可用 {{c1::prev2, prev1}} 滚动保存。

```
def solve(nums):
    prev2 = 0
    prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

**Evidence**

§1.2 打家劫舍

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.02%20-%20%E9%80%89%E6%88%96%E4%B8%8D%E9%80%89%E7%BA%BF%E6%80%A7%20DP)
