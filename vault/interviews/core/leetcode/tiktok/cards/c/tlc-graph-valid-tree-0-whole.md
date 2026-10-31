---
id: tlc-graph-valid-tree-0-whole
node: c.graph-valid-tree
type: qa
---
## Q
**LC 261 以图判树**｜Medium · LC TikTok 全时段热度 25/100

给定编号 `0..n - 1` 的 `n` 个节点和一个无向边列表 `edges`（`edges[i] = [a_i, b_i]`），判断这些边能否形成一棵合法有效的树。`1 <= n <= 2000`，`0 <= edges.length <= 5000`，`a_i != b_i`，没有自环和重复边。例：`n = 5`，`edges = [[0,1],[0,2],[0,3],[1,4]]` → `true`；`n = 5`，`edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]` → `false`（`1-2-3` 成环）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树等价于「恰好 `n - 1` 条边且无环」：先查边数，再用并查集逐条加边，遇到两端已经连通就是环。

**识别。** 「图是不是树」：树的三个等价刻画——连通且无环、连通且有 `n - 1` 条边、无环且有 `n - 1` 条边。选「边数 `n - 1` 加无环」，无环检测正是并查集的强项。

**推导。** 另一条路是 DFS 从 `0` 出发，检查访问到的点数为 `n` 且无环。并查集更短：边数不是 `n - 1` 直接否定；否则逐条加边，若某条边两端已在同一个集合，说明成环。`n - 1` 条边且无环，必然连通（`n` 个点的无环图连通分量数 = `n` - 边数 = `1`）。

```python
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:                      # 树恰好 n - 1 条边；多了必有环，少了必不连通
        return False
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]        # 路径折半
            x = parent[x]
        return x

    for a, b in edges:
        root_a, root_b = find(a), find(b)
        if root_a == root_b:                     # 两端早已连通：这条边闭合成环
            return False
        parent[root_a] = root_b
    return True                                  # n - 1 条边、无环 => 连通
```

运行：`(5, [[0,1],[0,2],[0,3],[1,4]])` → `True`，`(5, [[0,1],[1,2],[2,3],[1,3],[1,4]])` → `False`；`(1, [])` → `True`，`(2, [])` → `False`，`(4, [[0,1],[2,3]])` → `False`（边数不够）。

**复杂度。** 时间 `O(n · α(n))`，空间 `O(n)`。

**拓展优化。**
- 用 BFS 检查连通性，边数条件同样先判断：不依赖并查集，适合已经有邻接表的情形。

```python
from collections import defaultdict, deque


def valid_tree_bfs(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    seen = {0}
    queue = deque([0])
    while queue:
        for nxt in graph[queue.popleft()]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == n                        # n - 1 条边且连通 => 无环
```

- 同模式的计数问题（LC 323 连通分量数）：不要求边数，数并查集最后剩多少个根。

**易错点。**
- 只检查无环不检查边数：`n = 4`，`edges = [[0,1],[2,3]]` 无环，却不连通，不是树。
- 只检查连通不检查环：`n = 3`，`edges = [[0,1],[1,2],[0,2]]` 连通却有环，必须靠边数 `3 != 2` 才能拦下。
- 递归 DFS 做连通性检查：`n = 2000` 的链状图深度超过 1000，会抛 `RecursionError`；BFS 或并查集没有这个问题。

**追问。**
- 边是有向的（LC 684 的有向版 685）：需要处理入度 2 的节点，并查集加入度判断。
- 返回多余的那条边：并查集遇到成环的边就是答案（LC 684 冗余连接）。

**同模式。** LC 323 无向图中连通分量的数目、LC 684 冗余连接、LC 685 冗余连接 II、LC 547 省份数量、LC 1319 连通网络的操作次数。
