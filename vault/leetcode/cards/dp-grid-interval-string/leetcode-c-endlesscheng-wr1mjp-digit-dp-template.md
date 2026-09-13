---
id: leetcode-c-endlesscheng-wr1mjp-digit-dp-template
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272471881
tags: [concept-cloze, leetcode, recall, template]
---
数位 DP 常见状态为 {{c1::dfs(pos, property_state, tight, started)}}。

```
from functools import cache

def count_no_repeat(n):
    digits = list(map(int, str(n)))

    @cache
    def dfs(pos, mask, tight, started):
        if pos == len(digits):
            return int(started)
        upper = digits[pos] if tight else 9
        total = 0
        for d in range(upper + 1):
            next_started = started or d != 0
            if not next_started:
                total += dfs(pos + 1, mask, tight and d == upper, False)
            elif not (mask >> d) & 1:
                total += dfs(pos + 1, mask | (1 << d), tight and d == upper, True)
        return total

    return dfs(0, 0, True, False)
```

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.08%20-%20%E6%95%B0%E4%BD%8D%20DP)
