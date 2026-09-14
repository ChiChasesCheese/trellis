---
id: leetcode-c-endlesscheng-01luak-graph-floyd-warshall-template
node: shortest-path-uf-flow.graph-floyd-warshall
type: cloze
anki: 1787272410008
tags: [concept-cloze, leetcode, recall, template]
---
Floyd 模板的核心转移是 {{c1::f[i][j] = min(f[i][j], f[i][k] + f[k][j])}}。

```
import math

# f[i][j] = shortest distance from i to j, math.inf if unreachable
# negative edge weights are allowed; if any f[i][i] < 0 after this, there is a negative cycle
def solve(n: int, edges: list[list[int]]) -> list[list[float]]:
    f = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0

    for x, y, wt in edges:
        f[x][y] = min(f[x][y], wt)
        f[y][x] = min(f[y][x], wt)  # remove this line for a directed graph

    for k in range(n):
        for i in range(n):
            if f[i][k] == math.inf:
                continue
            for j in range(n):
                f[i][j] = min(f[i][j], f[i][k] + f[k][j])
    return f
```

**Evidence**

§3.2 全源最短路：Floyd 算法模板代码

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.08%20-%20%E5%85%A8%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9AFloyd%20%E7%AE%97%E6%B3%95)
