---
id: leetcode-c-endlesscheng-v2rxsn-binary-search-template
node: binary-search.binary-search
type: cloze
anki: 1787272463180
tags: [concept-cloze, leetcode, recall, template]
---
求最小可行值且 check(mid) 为真时，更新为 {{c1::hi = mid}}。

```
def min_feasible(lo, hi, check):
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Evidence**

一、技巧类题目：二分答案

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.02%20-%20%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E4%B8%8E%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
