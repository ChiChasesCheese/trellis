---
id: leetcode-c-endlesscheng-txls3i-convex-hull-and-wqs-dp-template
node: dp-linear-knapsack.convex-hull-and-wqs-dp
type: cloze
anki: 1787272416605
tags: [concept-cloze, leetcode, recall, template]
---
CHT 的每条候选可统一表示为 {{c1::(slope, intercept)}}。

```
def solve(lines, x):
    best = float('inf')
    for slope, intercept in lines:
        best = min(best, slope * x + intercept)
    return best
```

**Evidence**

§11.7 斜率优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.17%20-%20CHT%20%E4%B8%8E%20WQS%20%E4%BA%8C%E5%88%86%E4%BC%98%E5%8C%96)
