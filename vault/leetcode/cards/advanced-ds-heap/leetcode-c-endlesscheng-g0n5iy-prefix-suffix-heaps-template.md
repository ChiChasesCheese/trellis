---
id: leetcode-c-endlesscheng-g0n5iy-prefix-suffix-heaps-template
node: advanced-ds-heap.prefix-suffix-heaps
type: cloze
anki: 1787272479680
tags: [concept-cloze, leetcode, recall, template]
---
Python 用最小堆维护最小 k 项时，常把元素取负并在超过 k 时 {{c1::heappop(heap)}}。

```
import heapq

def smallest_k_sums(nums, k):
    heap = []
    total = 0
    result = [None] * len(nums)
    for i, x in enumerate(nums):
        heapq.heappush(heap, -x)
        total += x
        if len(heap) > k:
            total += heapq.heappop(heap)
        if len(heap) == k:
            result[i] = total
    return result
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.13%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%A0%86%E9%80%89%E6%8B%A9)
