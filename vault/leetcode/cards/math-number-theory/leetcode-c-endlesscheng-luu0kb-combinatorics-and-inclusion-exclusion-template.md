---
id: leetcode-c-endlesscheng-luu0kb-combinatorics-and-inclusion-exclusion-template
node: math-number-theory.combinatorics-and-inclusion-exclusion
type: cloze
anki: 1787272461679
tags: [concept-cloze, leetcode, recall, template]
---
变量 x_i 超过上界 limit_i 的容斥替换中，应令 x_i' = x_i - {{c1::(limit_i + 1)}}。

```
def count_bounded_solutions(total, limits):
    answer = 0
    m = len(limits)
    for mask in range(1 << m):
        remaining = total
        bits = 0
        for i in range(m):
            if mask >> i & 1:
                remaining -= limits[i] + 1
                bits += 1
        if remaining >= 0:
            ways = (remaining + m - 1) * (remaining + m - 2) // 2 if m == 3 else 0
            answer += -ways if bits % 2 else ways
    return answer
```

**Evidence**

五、数学：容斥原理

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.20%20-%20%E7%BB%84%E5%90%88%E8%AE%A1%E6%95%B0%E4%B8%8E%E5%AE%B9%E6%96%A5%E5%8E%9F%E7%90%86)
