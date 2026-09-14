---
id: leetcode-c-endlesscheng-g0n5iy-binary-search-on-answer-template
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272476680
tags: [concept-cloze, leetcode, recall, template]
---
最大可行二分为避免死循环，mid 写作 {{c1::(lo + hi + 1) // 2}}。

```
def max_feasible(lo, hi, check):
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**Evidence**

二分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
