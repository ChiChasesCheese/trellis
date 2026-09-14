---
id: leetcode-c-endlesscheng-txls3i-memoized-search-to-bottom-up-dp-template
node: dp-linear-knapsack.memoized-search-to-bottom-up-dp
type: cloze
anki: 1787272411805
tags: [concept-cloze, leetcode, recall, template]
---
记忆化递归通常用 {{c1::@cache}} 缓存 dfs 的返回值。

```
from functools import cache

def solve(n):
    @cache
    def dfs(i):
        if i <= 1:
            return 1
        return dfs(i - 1) + dfs(i - 2)
    return dfs(n)
```

**Evidence**

前言

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.01%20-%20%E8%AE%B0%E5%BF%86%E5%8C%96%E6%90%9C%E7%B4%A2%E4%B8%8E%E9%80%92%E6%8E%A8%20DP)
