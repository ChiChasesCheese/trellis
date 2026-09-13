---
id: leetcode-c-endlesscheng-01luak-graph-functional-graph-cycle-template
node: graphs-traversal.graph-functional-graph-cycle
type: cloze
anki: 1787272409405
tags: [concept-cloze, leetcode, recall, template]
---
基环树找环的做法本质是对内向图做类似拓扑排序的操作，反复剥除 {{c1::入度为 0}} 的节点，剩下的就是环。

```
from collections import deque

# next_node[i] is the single outgoing edge target of node i
def solve(n: int, next_node: list[int]) -> list[int]:
    in_deg = [0] * n
    for x in range(n):
        in_deg[next_node[x]] += 1

    on_cycle = [True] * n
    q = deque(i for i in range(n) if in_deg[i] == 0)
    while q:
        x = q.popleft()
        on_cycle[x] = False
        y = next_node[x]
        in_deg[y] -= 1
        if in_deg[y] == 0:
            q.append(y)

    cycle_nodes = [i for i in range(n) if on_cycle[i]]
    return cycle_nodes
```

**Evidence**

§2.3 基环树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.06%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91-%E5%86%85%E5%90%91%E5%9B%BE%E6%89%BE%E7%8E%AF%EF%BC%88%E6%8B%93%E6%89%91%E5%89%A5%E5%8F%B6%EF%BC%89)
