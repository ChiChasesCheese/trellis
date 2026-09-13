---
id: leetcode-c-endlesscheng-g6ktkl-merge-intervals-template
node: greedy-sorting.merge-intervals
type: cloze
anki: 1787272434307
tags: [concept-cloze, leetcode, recall, template]
---
发生重叠时右端点更新为 {{c1::max(merged[-1][1], right)}}。

```
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0][:]]
    for left, right in intervals[1:]:
        if left <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], right)
        else:
            merged.append([left, right])
    return merged
```

**Evidence**

§2.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.10%20-%20%E5%90%88%E5%B9%B6%E5%8C%BA%E9%97%B4)
