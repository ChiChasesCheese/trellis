---
id: leetcode-c-endlesscheng-txls3i-tree-dp-independent-set-diameter-domination-template
node: tree-advanced.tree-dp-independent-set-diameter-domination
type: cloze
anki: 1787272416905
tags: [concept-cloze, leetcode, recall, template]
---
最大独立集里选 node 时，应累加每个孩子的 {{c1::skip}} 状态。

```
def solve(values, edges):
    n = len(values)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    def dfs(node, parent):
        take = values[node]
        skip = 0
        for nxt in graph[node]:
            if nxt != parent:
                child_take, child_skip = dfs(nxt, node)
                take += child_skip
                skip += max(child_take, child_skip)
        return take, skip
    return max(dfs(0, -1))
```

**Evidence**

§12.2 树上最大独立集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.18%20-%20%E6%A0%91%E5%BD%A2%20DP%EF%BC%9A%E7%9B%B4%E5%BE%84%E3%80%81%E7%8B%AC%E7%AB%8B%E9%9B%86%E4%B8%8E%E6%94%AF%E9%85%8D%E9%9B%86)
