---
id: leetcode-c-endlesscheng-v2rxsn-heap-priority-queue-template
node: advanced-ds-heap.heap-priority-queue
type: cloze
anki: 1787272467081
tags: [concept-cloze, leetcode, recall, template]
---
维护 k 个最大值时，堆长度超过 k 就 {{c1::heappop}} 删除最小值。

```
import heapq

def k_largest(nums, k):
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

**Evidence**

四、数据结构：堆（优先队列）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.15%20-%20%E5%A0%86%E4%B8%8E%E4%BC%98%E5%85%88%E9%98%9F%E5%88%97)
