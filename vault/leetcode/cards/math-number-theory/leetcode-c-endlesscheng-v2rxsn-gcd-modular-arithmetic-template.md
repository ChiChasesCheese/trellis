---
id: leetcode-c-endlesscheng-v2rxsn-gcd-modular-arithmetic-template
node: math-number-theory.gcd-modular-arithmetic
type: cloze
anki: 1787272468880
tags: [concept-cloze, leetcode, recall, template]
---
判断 target 是否属于步长整数线性组合，检查 {{c1::target % g == 0}}。

```
from math import gcd

def reachable(steps, target):
    g = 0
    for step in steps:
        g = gcd(g, abs(step))
    return g != 0 and target % g == 0
```

**Evidence**

五、数学：GCD

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.21%20-%20GCD%E3%80%81%E5%90%8C%E4%BD%99%E4%B8%8E%E8%A3%B4%E8%9C%80%E5%AE%9A%E7%90%86)
