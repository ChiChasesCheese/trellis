---
id: leetcode-c-endlesscheng-txls3i-permutation-bitmask-dp-template
node: dp-grid-interval-string.permutation-bitmask-dp
type: cloze
anki: 1787272415107
tags: [concept-cloze, leetcode, recall, template]
---
向 mask 加入 nxt 的写法是 {{c1::mask | (1 << nxt)}}。

```
def solve(cost):
    n = len(cost)
    inf = float('inf')
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last & 1):
                continue
            for nxt in range(n):
                if not (mask >> nxt & 1):
                    dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt], dp[mask][last] + cost[last][nxt])
    return min(dp[-1])
```

**Evidence**

§9.3 旅行商问题（TSP）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.12%20-%20%E6%8E%92%E5%88%97%E5%9E%8B%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%20DP%20%E4%B8%8E%20TSP)
