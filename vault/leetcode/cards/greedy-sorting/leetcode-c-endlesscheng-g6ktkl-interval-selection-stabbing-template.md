---
id: leetcode-c-endlesscheng-g6ktkl-interval-selection-stabbing-template
node: greedy-sorting.interval-selection-stabbing
type: cloze
anki: 1787272433404
tags: [concept-cloze, leetcode, recall, template]
---
不相交区间扫描中，满足兼容条件后更新 {{c1::end = right}}。

```
def max_non_overlapping(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda p: p[1])
    count = 0
    end = float('-inf')
    for left, right in intervals:
        if left >= end:
            count += 1
            end = right
    return count
```

**Evidence**

§2.1

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.07%20-%20%E4%B8%8D%E7%9B%B8%E4%BA%A4%E5%8C%BA%E9%97%B4%E4%B8%8E%E5%8C%BA%E9%97%B4%E9%80%89%E7%82%B9)
