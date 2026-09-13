---
id: leetcode-c-endlesscheng-g0n5iy-gcd-divisor-counting-template
node: math-number-theory.gcd-divisor-counting
type: cloze
anki: 1787272477279
tags: [concept-cloze, leetcode, recall, template]
---
处理当前 gcd 为 g 时，可遍历历史 h 并检查 {{c1::g * h % k == 0}}。

```
from collections import Counter
from math import gcd

def count_pairs(nums, k):
    freq = Counter()
    ans = 0
    for x in nums:
        g = gcd(x, k)
        for h, count in freq.items():
            if g * h % k == 0:
                ans += count
        freq[g] += 1
    return ans
```

**Evidence**

数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.05%20-%20%E6%9C%80%E5%A4%A7%E5%85%AC%E7%BA%A6%E6%95%B0%E4%B8%8E%E5%9B%A0%E5%AD%90%E8%AE%A1%E6%95%B0)
