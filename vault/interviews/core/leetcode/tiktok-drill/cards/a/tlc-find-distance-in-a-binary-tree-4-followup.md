---
id: tlc-find-distance-in-a-binary-tree-4-followup
node: a.find-distance-in-a-binary-tree
type: qa
step: 4
---
## Q
**LC 1740 找到二叉树中的距离**｜追问

面试官接着问：（1）要返回具体路径而不是长度？（2）同一棵树要回答很多次 `(p, q)` 查询？（3）树是 `n` 个结点的 N 叉树或只给了边表？

## A
1. **返回路径**：爬升时把 `a` 经过的结点追加到 `left_part`，把 `b` 经过的追加到 `right_part`，相遇后 `left_part + [lca] + right_part[::-1]`。关键是别漏掉相遇点，也别重复。
2. **多次查询**：预处理一次 `parent` / `depth`，再建倍增表 `up[k][v]`（`v` 的第 `2^k` 个祖先），每次查询 `O(log n)`；离线批量查询可用 Tarjan 离线 LCA，近似 `O(n + q)`。
3. **N 叉树 / 边表**：不用区分 `left` / `right`，把边建成邻接表 `defaultdict(list)`，从 `p` 做 BFS 到 `q`，层数即距离，`O(n)`；这个做法对任意无环连通图都成立，是兜底写法。

```python
from collections import defaultdict, deque

def tree_distance(edges: list[tuple[int, int]], p: int, q: int) -> int:
    adj: defaultdict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = {p: 0}
    dq = deque([p])
    while dq:
        u = dq.popleft()
        if u == q:
            return dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    return -1
```

**Python 提醒**：`defaultdict` 读不存在的键会**插入**一个空列表；判断存在要用 `in`，别用 `adj[x]` 试探。
