---
id: leetcode-c-endlesscheng-txls3i-rerooting-dp-template
node: tree-advanced.rerooting-dp
type: cloze
anki: 1787272417206
tags: [concept-cloze, leetcode, recall, template]
---
换根通常分为 {{c1::一次向下 DFS 和一次向上 DFS}}。

```
def solve(n, edges):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    size = [0] * n
    ans = [0] * n
    def dfs(u, p):
        size[u] = 1
        for v in graph[u]:
            if v != p:
                dfs(v, u)
                size[u] += size[v]
    def reroot(u, p):
        for v in graph[u]:
            if v != p:
                ans[v] = ans[u] - size[v] + (n - size[v])
                reroot(v, u)
    dfs(0, -1)
    reroot(0, -1)
    return ans
```

**Evidence**

§12.4 换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.19%20-%20%E6%8D%A2%E6%A0%B9%20DP)
