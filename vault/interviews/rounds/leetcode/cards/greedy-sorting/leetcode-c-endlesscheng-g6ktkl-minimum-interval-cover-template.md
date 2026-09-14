---
id: leetcode-c-endlesscheng-g6ktkl-minimum-interval-cover-template
node: greedy-sorting.minimum-interval-cover
type: cloze
anki: 1787272434006
tags: [concept-cloze, leetcode, recall, template]
---
若一轮扫描后 farthest == current，模板应返回 {{c1::-1}}。

```
def min_cover(intervals: list[list[int]], start: int, target: int) -> int:
    intervals.sort()
    i = 0
    current = start
    used = 0
    while current < target:
        farthest = current
        while i < len(intervals) and intervals[i][0] <= current:
            farthest = max(farthest, intervals[i][1])
            i += 1
        if farthest == current:
            return -1
        current = farthest
        used += 1
    return used
```

**Evidence**

§2.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.09%20-%20%E6%9C%80%E5%B0%91%E5%8C%BA%E9%97%B4%E8%A6%86%E7%9B%96)
