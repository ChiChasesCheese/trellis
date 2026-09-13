---
id: leetcode-c-endlesscheng-iyt3ss-divisor-enumeration-template
node: math-number-theory.divisor-enumeration
type: cloze
anki: 1787272425907
tags: [concept-cloze, leetcode, recall, template]
---
全范围约数表的内层循环是 range({{c1::d, limit + 1, d}})。

```
def all_divisors(limit):
    divisors = [[] for _ in range(limit + 1)]
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            divisors[multiple].append(d)
    return divisors
```

**Evidence**

§1.5 因子

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.04%20-%20%E7%BA%A6%E6%95%B0%E6%9E%9A%E4%B8%BE%E4%B8%8E%E5%80%8D%E6%95%B0%E9%A2%84%E5%A4%84%E7%90%86)
