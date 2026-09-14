---
id: leetcode-c-endlesscheng-wr1mjp-tree-dp-and-center-expansion-template
node: tree-advanced.tree-dp-and-center-expansion
type: cloze
anki: 1787272472181
tags: [concept-cloze, leetcode, recall, template]
---
中心扩展应枚举 {{c1::奇数中心 (i,i) 和偶数中心 (i,i+1)}}。

```
def tree_independent_set(n, edges, value):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def dfs(node, parent):
        take = value[node]
        skip = 0
        for nxt in graph[node]:
            if nxt == parent:
                continue
            child_take, child_skip = dfs(nxt, node)
            take += child_skip
            skip += max(child_take, child_skip)
        return take, skip

    return max(dfs(0, -1))
```

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.09%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95)
