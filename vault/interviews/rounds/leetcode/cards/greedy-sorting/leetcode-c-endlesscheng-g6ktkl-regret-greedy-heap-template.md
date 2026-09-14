---
id: leetcode-c-endlesscheng-g6ktkl-regret-greedy-heap-template
node: greedy-sorting.regret-greedy-heap
type: cloze
anki: 1787272433104
tags: [concept-cloze, leetcode, recall, template]
---
Python 中要弹出最大代价，入堆值应为 {{c1::-cost}}。

```
import heapq

def max_count(costs: list[int], budget: int) -> int:
    chosen: list[int] = []
    total = 0
    for cost in costs:
        total += cost
        heapq.heappush(chosen, -cost)
        if total > budget:
            total += heapq.heappop(chosen)
    return len(chosen)
```

**Evidence**

§1.9

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.06%20-%20%E5%8F%8D%E6%82%94%E8%B4%AA%E5%BF%83)
