---
id: leetcode-c-endlesscheng-g6ktkl-rearrangement-inequality-template
node: greedy-sorting.rearrangement-inequality
type: cloze
anki: 1787272435806
tags: [concept-cloze, leetcode, recall, template]
---
最大点积模板应将 a、b 都 {{c1::升序排序}} 后 zip 求和。

```
def max_dot_product(a: list[int], b: list[int]) -> int:
    a.sort()
    b.sort()
    return sum(x * y for x, y in zip(a, b))
```

**Evidence**

§4.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.15%20-%20%E6%8E%92%E5%BA%8F%E4%B8%8D%E7%AD%89%E5%BC%8F)
