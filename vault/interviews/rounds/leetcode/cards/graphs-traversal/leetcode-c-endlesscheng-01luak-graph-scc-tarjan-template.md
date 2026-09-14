---
id: leetcode-c-endlesscheng-01luak-graph-scc-tarjan-template
node: graphs-traversal.graph-scc-tarjan
type: cloze
anki: 1787272410904
tags: [concept-cloze, leetcode, recall, template]
---
Tarjan 算法中判断邻居 y 是否仍在当前搜索路径栈上、从而可以用来更新 low[x] 的条件是 {{c1::on_stack[y]}}。

```
import sys

def solve(n: int, edges: list[list[int]]) -> list[int]:
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)

    dfn = [0] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []
    timer = [0]
    scc_id = [-1] * n
    scc_count = [0]

    sys.setrecursionlimit(max(10000, n * 2))

    def dfs(x: int) -> None:
        timer[0] += 1
        dfn[x] = low[x] = timer[0]
        stack.append(x)
        on_stack[x] = True
        for y in g[x]:
            if dfn[y] == 0:
                dfs(y)
                low[x] = min(low[x], low[y])
            elif on_stack[y]:
                low[x] = min(low[x], dfn[y])
        if low[x] == dfn[x]:
            while True:
                y = stack.pop()
                on_stack[y] = False
                scc_id[y] = scc_count[0]
                if y == x:
                    break
            scc_count[0] += 1

    for i in range(n):
        if dfn[i] == 0:
            dfs(i)
    return scc_id
```

**Evidence**

六、强连通分量/双连通分量

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.11%20-%20%E5%BC%BA%E8%BF%9E%E9%80%9A%E5%88%86%E9%87%8F%EF%BC%9ATarjan%20%E7%AE%97%E6%B3%95)
