---
id: leetcode-c-endlesscheng-luu0kb-floyd-warshall-template
node: shortest-path-uf-flow.floyd-warshall
type: cloze
anki: 1787272459280
tags: [concept-cloze, leetcode, recall, template]
---
Floyd 的核心更新是 dist[i][j] = min(dist[i][j], {{c1::dist[i][k] + dist[k][j]}})。

```
def floyd_warshall(n, edges):
    inf = float('inf')
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, weight in edges:
        dist[u][v] = min(dist[u][v], weight)
    for mid in range(n):
        for start in range(n):
            for end in range(n):
                dist[start][end] = min(dist[start][end],
                                       dist[start][mid] + dist[mid][end])
    return dist
```

**Evidence**

三、图论：Floyd

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.12%20-%20%E5%9B%BE%E8%AE%BA%EF%BC%9AFloyd-Warshall)
