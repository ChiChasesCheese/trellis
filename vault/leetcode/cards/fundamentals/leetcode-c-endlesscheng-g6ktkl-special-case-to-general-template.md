---
id: leetcode-c-endlesscheng-g6ktkl-special-case-to-general-template
node: fundamentals.special-case-to-general
type: cloze
anki: 1787272436706
tags: [concept-cloze, leetcode, recall, template]
---
枚举长度 n 的二元数组可用 {{c1::product((0, 1), repeat=n)}}。

```
from itertools import product

def inspect_binary_patterns(n: int) -> list[tuple[int, ...]]:
    patterns = []
    for values in product((0, 1), repeat=n):
        if sum(values) * 2 >= n:
            patterns.append(values)
    return patterns
```

**Evidence**

§5.1

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.18%20-%20%E4%BB%8E%E7%89%B9%E6%AE%8A%E5%88%B0%E4%B8%80%E8%88%AC%E7%9A%84%E5%8F%8D%E4%BE%8B%E4%B8%8E%E5%BD%92%E7%BA%B3%E6%8E%A2%E7%B4%A2)
