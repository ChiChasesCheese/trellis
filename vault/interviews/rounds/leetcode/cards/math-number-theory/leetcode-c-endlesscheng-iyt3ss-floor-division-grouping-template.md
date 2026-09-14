---
id: leetcode-c-endlesscheng-iyt3ss-floor-division-grouping-template
node: math-number-theory.floor-division-grouping
type: cloze
anki: 1787272426506
tags: [concept-cloze, leetcode, recall, template]
---
每一块处理后应令 left = {{c1::right + 1}}。

```
def grouped_quotients(n):
    groups = []
    left = 1
    while left <= n:
        q = n // left
        right = n // q
        groups.append((left, right, q))
        left = right + 1
    return groups
```

**Evidence**

§1.10 数论分块

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.06%20-%20%E6%95%B0%E8%AE%BA%E5%88%86%E5%9D%97)
