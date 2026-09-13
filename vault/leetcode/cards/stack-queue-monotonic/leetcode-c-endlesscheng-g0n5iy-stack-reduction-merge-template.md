---
id: leetcode-c-endlesscheng-g0n5iy-stack-reduction-merge-template
node: stack-queue-monotonic.stack-reduction-merge
type: cloze
anki: 1787272480279
tags: [concept-cloze, leetcode, recall, template]
---
连锁合并的关键结构是 {{c1::while stack:}}，而不是单次 if。

```
from math import gcd

def merge_non_coprime(nums):
    stack = []
    for x in nums:
        while stack:
            g = gcd(stack[-1], x)
            if g == 1:
                break
            x = stack.pop() // g * x
        stack.append(x)
    return stack
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.15%20-%20%E6%A0%88%E5%BC%8F%E5%BD%92%E7%BA%A6%E5%90%88%E5%B9%B6)
