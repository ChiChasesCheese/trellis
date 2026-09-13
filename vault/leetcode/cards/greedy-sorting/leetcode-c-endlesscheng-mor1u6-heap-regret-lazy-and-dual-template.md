---
id: leetcode-c-endlesscheng-mor1u6-heap-regret-lazy-and-dual-template
node: greedy-sorting.heap-regret-lazy-and-dual
type: cloze
anki: 1789002114320
tags: [concept-cloze, leetcode, recall, template]
---
中位数对顶堆需维持两堆大小差 {{c1::至多为一}}。

```
import heapq

def running_medians(nums):
    low, high, ans = [], [], []
    for x in nums:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))
        if len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        ans.append(-low[0])
    return ans
```

**Evidence**

§5.7 对顶堆（动态第 K 小/大）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.10%20-%20%E5%8F%8D%E6%82%94%E5%A0%86%E3%80%81%E6%87%92%E5%88%A0%E9%99%A4%E5%A0%86%E4%B8%8E%E5%AF%B9%E9%A1%B6%E5%A0%86)
