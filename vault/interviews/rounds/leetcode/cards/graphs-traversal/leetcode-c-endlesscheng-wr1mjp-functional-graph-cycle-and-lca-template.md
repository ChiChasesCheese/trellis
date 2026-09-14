---
id: leetcode-c-endlesscheng-wr1mjp-functional-graph-cycle-and-lca-template
node: graphs-traversal.functional-graph-cycle-and-lca
type: cloze
anki: 1787272474880
tags: [concept-cloze, leetcode, recall, template]
---
函数图环长可由 {{c1::当前时间 - 该节点首次时间戳}} 计算。

```
def longest_cycle(next_node):
    n = len(next_node)
    seen = [0] * n
    answer = -1
    clock = 1
    for start in range(n):
        if seen[start]:
            continue
        local = {}
        node = start
        while node != -1 and not seen[node]:
            seen[node] = clock
            local[node] = clock
            clock += 1
            node = next_node[node]
        if node in local:
            answer = max(answer, clock - local[node])
    return answer
```

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.18%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E6%97%B6%E9%97%B4%E6%88%B3%E4%B8%8E%20LCA)
