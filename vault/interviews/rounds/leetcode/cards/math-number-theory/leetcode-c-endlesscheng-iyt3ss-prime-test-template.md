---
id: leetcode-c-endlesscheng-iyt3ss-prime-test-template
node: math-number-theory.prime-test
type: cloze
anki: 1787272425004
tags: [concept-cloze, leetcode, recall, template]
---
判质数模板应先处理 {{c1::n < 2}}，再枚举 d 到 isqrt(n)。

```
from math import isqrt

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return False
    return True
```

**Evidence**

§1.1 判断质数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.01%20-%20%E5%B9%B3%E6%96%B9%E6%A0%B9%E8%AF%95%E9%99%A4%E5%88%A4%E8%B4%A8%E6%95%B0)
