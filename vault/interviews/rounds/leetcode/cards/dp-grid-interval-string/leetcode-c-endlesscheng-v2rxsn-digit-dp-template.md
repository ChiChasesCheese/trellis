---
id: leetcode-c-endlesscheng-v2rxsn-digit-dp-template
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272465881
tags: [concept-cloze, leetcode, recall, template]
---
tight 状态转移为 tight and {{c1::digit == upper}}。

```
from functools import lru_cache

def count_leq(limit):
    digits = list(map(int, str(limit)))
    @lru_cache(None)
    def dfs(i, tight):
        if i == len(digits):
            return 1
        upper = digits[i] if tight else 9
        total = 0
        for digit in range(upper + 1):
            total += dfs(i + 1, tight and digit == upper)
        return total
    return dfs(0, True)
```

**Evidence**

二、动态规划：数位 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.11%20-%20%E6%95%B0%E4%BD%8D%20DP)
