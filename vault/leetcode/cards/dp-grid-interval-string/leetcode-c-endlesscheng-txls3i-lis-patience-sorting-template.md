---
id: leetcode-c-endlesscheng-txls3i-lis-patience-sorting-template
node: dp-grid-interval-string.lis-patience-sorting
type: cloze
anki: 1787272413604
tags: [concept-cloze, leetcode, recall, template]
---
严格递增 LIS 用 {{c1::bisect_left}} 找替换位置。

```
from bisect import bisect_left

def solve(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**Evidence**

§4.2 最长递增子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.07%20-%20LIS%20%E4%B8%8E%E8%80%90%E5%BF%83%E6%8E%92%E5%BA%8F)
