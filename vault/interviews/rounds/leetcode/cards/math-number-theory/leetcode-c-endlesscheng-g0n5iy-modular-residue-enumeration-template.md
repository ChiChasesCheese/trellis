---
id: leetcode-c-endlesscheng-g0n5iy-modular-residue-enumeration-template
node: math-number-theory.modular-residue-enumeration
type: cloze
anki: 1787272477879
tags: [concept-cloze, leetcode, recall, template]
---
个位循环问题中，可至多枚举 {{c1::10}} 次来覆盖所有模 10 状态。

```
def min_count_for_residue(target, unit):
    for count in range(1, 11):
        if (count * unit - target) % 10 == 0:
            return count
    return -1
```

**Evidence**

数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.07%20-%20%E5%90%8C%E4%BD%99%E7%B1%BB%E6%9E%9A%E4%B8%BE)
