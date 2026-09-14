---
id: leetcode-c-endlesscheng-g6ktkl-interval-grouping-heap-template
node: greedy-sorting.interval-grouping-heap
type: cloze
anki: 1787272433704
tags: [concept-cloze, leetcode, recall, template]
---
当前区间能复用组时，先执行 {{c1::heapq.heappop(ends)}} 再压入其右端点。

```
import heapq

def min_groups(intervals: list[list[int]]) -> int:
    intervals.sort()
    ends: list[int] = []
    for left, right in intervals:
        if ends and ends[0] < left:
            heapq.heappop(ends)
        heapq.heappush(ends, right)
    return len(ends)
```

**Evidence**

§2.2

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.08%20-%20%E5%8C%BA%E9%97%B4%E5%88%86%E7%BB%84)
