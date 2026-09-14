---
id: leetcode-c-endlesscheng-01luak-graph-bfs-state-space-modeling-template
node: graphs-traversal.graph-bfs-state-space-modeling
type: cloze
anki: 1787272408503
tags: [concept-cloze, leetcode, recall, template]
---
状态空间 BFS 模板中，判断某个后继状态 nxt 是否需要入队的条件是 {{c1::nxt not in dis}}。

```
from collections import deque
from typing import Callable, Hashable

def solve(start_state: Hashable, is_target: Callable[[Hashable], bool],
          get_neighbors: Callable[[Hashable], list]) -> int:
    dis = {start_state: 0}
    q = deque([start_state])
    while q:
        state = q.popleft()
        if is_target(state):
            return dis[state]
        for nxt in get_neighbors(state):
            if nxt not in dis:
                dis[nxt] = dis[state] + 1
                q.append(nxt)
    return -1  # target unreachable
```

**Evidence**

§1.3 图论建模 + BFS 最短路

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.03%20-%20%E5%9B%BE%E8%AE%BA%E5%BB%BA%E6%A8%A1%20%2B%20BFS%20%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%90%9C%E7%B4%A2%EF%BC%89)
