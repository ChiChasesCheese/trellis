---
id: leetcode-c-endlesscheng-iyt3ss-inclusion-exclusion-template
node: math-number-theory.inclusion-exclusion
type: cloze
anki: 1787272427404
tags: [concept-cloze, leetcode, recall, template]
---
子集 mask 的交集项在 bit_count 为奇数时 {{c1::相加}}，偶数时相减。

```
def union_size(intersection_size, count):
    total = 0
    for mask in range(1, 1 << count):
        bits = mask.bit_count()
        value = intersection_size(mask)
        total += value if bits % 2 else -value
    return total
```

**Evidence**

§2.4 容斥原理

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.09%20-%20%E5%AE%B9%E6%96%A5%E5%8E%9F%E7%90%86)
