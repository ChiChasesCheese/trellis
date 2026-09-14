---
id: leetcode-c-endlesscheng-luu0kb-binary-search-on-answer-template
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272456281
tags: [concept-cloze, leetcode, recall, template]
---
二分答案的复杂度骨架是 {{c1::O(log R × check)}}。

```
def minimum_feasible(low, high, feasible):
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid + 1
    return low
```

**Evidence**

一、技巧类题目：二分答案

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.02%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
