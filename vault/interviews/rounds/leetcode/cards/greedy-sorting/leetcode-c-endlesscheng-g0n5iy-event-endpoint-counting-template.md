---
id: leetcode-c-endlesscheng-g0n5iy-event-endpoint-counting-template
node: greedy-sorting.event-endpoint-counting
type: cloze
anki: 1787272476980
tags: [concept-cloze, leetcode, recall, template]
---
闭区间覆盖查询的 Python 写法是 bisect_right(starts, t) - {{c1::bisect_left(ends, t)}}。

```
from bisect import bisect_right, bisect_left

def active_counts(intervals, queries):
    starts = sorted(left for left, _ in intervals)
    ends = sorted(right for _, right in intervals)
    return [bisect_right(starts, t) - bisect_left(ends, t) for t in queries]
```

**Evidence**

二分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.04%20-%20%E4%BA%8B%E4%BB%B6%E7%AB%AF%E7%82%B9%E8%AE%A1%E6%95%B0)
