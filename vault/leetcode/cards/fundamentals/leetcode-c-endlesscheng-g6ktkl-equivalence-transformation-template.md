---
id: leetcode-c-endlesscheng-g6ktkl-equivalence-transformation-template
node: fundamentals.equivalence-transformation
type: cloze
anki: 1787272437005
tags: [concept-cloze, leetcode, recall, template]
---
“最大保留量”常可改写为 {{c1::total - removed_sum}}。

```
def max_kept(total: int, removed: list[int]) -> int:
    return total - sum(removed)
```

**Evidence**

§5.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.19%20-%20%E7%AD%89%E4%BB%B7%E8%BD%AC%E5%8C%96)
