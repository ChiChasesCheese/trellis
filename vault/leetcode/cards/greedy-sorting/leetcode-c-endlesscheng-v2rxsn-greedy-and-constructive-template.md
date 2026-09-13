---
id: leetcode-c-endlesscheng-v2rxsn-greedy-and-constructive-template
node: greedy-sorting.greedy-and-constructive
type: cloze
anki: 1787272469180
tags: [concept-cloze, leetcode, recall, template]
---
区间选择的经典贪心是按结束时间排序，并选择 {{c1::当前可兼容的最早结束区间}}。

```
def select_max_non_overlapping(intervals):
    intervals.sort(key=lambda item: item[1])
    chosen = 0
    end = float('-inf')
    for start, finish in intervals:
        if start >= end:
            chosen += 1
            end = finish
    return chosen
```

**Evidence**

六、思维题：贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.22%20-%20%E8%B4%AA%E5%BF%83%E4%B8%8E%E6%9E%84%E9%80%A0)
