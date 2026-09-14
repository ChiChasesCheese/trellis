---
id: leetcode-c-endlesscheng-mor1u6-heap-selection-and-rearrangement-template
node: advanced-ds-heap.heap-selection-and-rearrangement
type: cloze
anki: 1787272421107
tags: [concept-cloze, leetcode, recall, template]
---
第 K 大模板在 push 后若 len(heap)>K，则 {{c1::heappop(heap)}}。

```
import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

**Evidence**

§5.3 第 K 小/大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.11%20-%20%E5%A0%86%E7%9A%84%E9%80%89%E6%8B%A9%E4%B8%8E%E9%87%8D%E6%8E%92)
