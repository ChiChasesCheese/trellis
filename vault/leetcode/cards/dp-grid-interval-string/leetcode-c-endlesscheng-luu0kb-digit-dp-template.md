---
id: leetcode-c-endlesscheng-luu0kb-digit-dp-template
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272458678
tags: [concept-cloze, leetcode, recall, template]
---
区间 [L,R] 的数位 DP 统计通常计算 {{c1::count(R) - count(L - 1)}}。

```
from functools import lru_cache

def count_no_adjacent_equal(limit):
    digits = list(map(int, str(limit)))

    @lru_cache(None)
    def dfs(pos, previous, tight, started):
        if pos == len(digits):
            return 1
        upper = digits[pos] if tight else 9
        total = 0
        for digit in range(upper + 1):
            next_started = started or digit != 0
            if next_started and started and digit == previous:
                continue
            total += dfs(pos + 1, digit if next_started else 10,
                         tight and digit == upper, next_started)
        return total

    return dfs(0, 10, True, False)
```

**Evidence**

二、动态规划：数位 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.10%20-%20%E6%95%B0%E4%BD%8D%20DP)
