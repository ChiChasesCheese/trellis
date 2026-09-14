---
id: leetcode-c-endlesscheng-luu0kb-regret-greedy-with-heap-template
node: greedy-sorting.regret-greedy-with-heap
type: cloze
anki: 1787272462279
tags: [concept-cloze, leetcode, recall, template]
---
维护最多 k 个最大值时，用最小堆；超出 k 后弹出 {{c1::堆顶}}。

```
import heapq

def maximize_sum_with_k_choices(values, k):
    chosen = []
    total = 0
    for value in values:
        heapq.heappush(chosen, value)
        total += value
        if len(chosen) > k:
            total -= heapq.heappop(chosen)
    return total
```

**Evidence**

六、思维题：反悔贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.22%20-%20%E5%8F%8D%E6%82%94%E8%B4%AA%E5%BF%83)
