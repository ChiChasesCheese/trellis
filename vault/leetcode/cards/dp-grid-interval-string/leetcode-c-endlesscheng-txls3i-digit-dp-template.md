---
id: leetcode-c-endlesscheng-txls3i-digit-dp-template
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272415706
tags: [concept-cloze, leetcode, recall, template]
---
数位贡献 DP 常让 dfs 同时返回 {{c1::数量和贡献和}}。

```
from functools import cache

def solve(limit):
    digits = list(map(int, str(limit)))
    @cache
    def dfs(i, tight):
        if i == len(digits):
            return 1
        upper = digits[i] if tight else 9
        return sum(dfs(i + 1, tight and d == upper) for d in range(upper + 1))
    return dfs(0, True)
```

**Evidence**

§10.2 统计合法元素的价值总和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.14%20-%20%E6%95%B0%E4%BD%8D%20DP%EF%BC%9A%E8%AE%A1%E6%95%B0%E4%B8%8E%E8%B4%A1%E7%8C%AE)
