---
id: leetcode-c-endlesscheng-01luak-graph-dfs-connected-components-template
node: graphs-traversal.graph-dfs-connected-components
type: cloze
anki: 1787272407903
tags: [concept-cloze, leetcode, recall, template]
---
DFS 连通块模板中，递归函数在访问节点 x 时首先要做的是 {{c1::vis[x] = True}}，防止后续重复访问。

```
def solve(n: int, edges: list[list[int]]) -> list[int]:
    # build undirected adjacency list, nodes numbered 0..n-1
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)

    vis = [False] * n

    def dfs(x: int) -> int:
        vis[x] = True
        size = 1
        for y in g[x]:
            if not vis[y]:
                size += dfs(y)
        return size

    sizes = []
    for i in range(n):
        if not vis[i]:
            sizes.append(dfs(i))
    return sizes
```

**Evidence**

§1.1 深度优先搜索（DFS）模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.01%20-%20DFS%20%E6%B1%82%E8%BF%9E%E9%80%9A%E5%9D%97-%E5%88%A4%E7%8E%AF)
