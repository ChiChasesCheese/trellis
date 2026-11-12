---
slug: possible-bipartition
---
## Q
**LC 886 可能的二分法**｜Medium

编号 `1..n` 的人分成两组，`dislikes[i] = [a, b]` 表示两人不能同组。判断能否分成功。

## A
**一句话。** 互相讨厌建无向图，判断是否二分图：BFS 给每个连通块染色，相邻同色即失败。

```python
def possible_bipartition(n, dislikes):
    graph = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    color = [0] * (n + 1)        # 0 未染色，1 / -1 两组
    for start in range(1, n + 1):
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:
                    return False
                if color[v] == 0:
                    color[v] = -color[u]
                    queue.append(v)
    return True
```

**复杂度。** 时间 `O(n+m)`，空间 `O(n+m)`。

**易错点。**
- 只从 `1` 出发一次：`n=6`、`[[1,2],[3,4],[4,5],[3,5]]` 的三角形在另一个连通块，会得 `True`，应为 `False`。
- 只在未染色时染色、不查已染色邻居：漏掉奇数环。

**追问。**
- 能用 DFS 吗？：能，染色逻辑相同，但链状图的递归会超默认深度，所以用 BFS。
- 分成 `k >= 3` 组？：就是图 `k` 着色，NP 完全，只能回溯或启发式。
- 边在线加入、每次都要答？：并查集记录「敌人」关系。

**同模式。** LC 785 判断二分图、LC 1042 不邻接植花、LC 802 找到最终的安全状态、LC 261 以图判树
