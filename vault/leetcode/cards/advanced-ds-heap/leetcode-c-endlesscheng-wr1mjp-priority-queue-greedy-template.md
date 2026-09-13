---
id: leetcode-c-endlesscheng-wr1mjp-priority-queue-greedy-template
node: advanced-ds-heap.priority-queue-greedy
type: cloze
anki: 1787272472781
tags: [concept-cloze, leetcode, recall, template]
---
Python 最小堆插入和取出分别是 {{c1::heapq.heappush(heap, x) 与 heapq.heappop(heap)}}。

```
import heapq

def assign_rooms(intervals):
    intervals.sort()
    busy = []
    for start, end in intervals:
        if busy and busy[0] <= start:
            heapq.heapreplace(busy, end)
        else:
            heapq.heappush(busy, end)
    return len(busy)
```

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.11%20-%20%E5%A0%86%E4%B8%8E%E4%BC%98%E5%85%88%E9%98%9F%E5%88%97)
