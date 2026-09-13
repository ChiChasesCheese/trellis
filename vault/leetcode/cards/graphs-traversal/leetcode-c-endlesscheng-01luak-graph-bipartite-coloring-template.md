---
id: leetcode-c-endlesscheng-01luak-graph-bipartite-coloring-template
node: graphs-traversal.graph-bipartite-coloring
type: cloze
anki: 1787272411208
tags: [concept-cloze, leetcode, recall, template]
---
交替染色法中，递归给邻居染色时使用的颜色是 {{c1::3 - c}}，即两种颜色互相切换。

```
def solve(n: int, edges: list[list[int]]) -> list[int]:
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)

    # colors[i] = 0: unvisited, 1: color A, 2: color B
    colors = [0] * n

    def dfs(x: int, c: int) -> bool:
        colors[x] = c
        for y in g[x]:
            if colors[y] == c or (colors[y] == 0 and not dfs(y, 3 - c)):
                return False
        return True

    for i in range(n):
        if colors[i] == 0 and not dfs(i, 1):
            return []
    return colors
```

**Evidence**

七、二分图染色模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.12%20-%20%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%EF%BC%88%E4%BA%A4%E6%9B%BF%E6%9F%93%E8%89%B2%E6%B3%95%EF%BC%89)
