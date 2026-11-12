---
slug: course-schedule-iv
---
## Q
**LC 1462 课程表 IV**｜Medium

`[a, b]` 表示选 `b` 前须先选 `a`，先修关系可以间接传递。对每个查询 `[u, v]`，回答 `u` 是否是 `v` 的先修课。

## A
**一句话。** 按拓扑序预处理传递闭包，用整数位集记录每门课的全部先修课，查询 `O(1)`。

```python
def check_if_prerequisite(num_courses, prereqs, queries):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prereqs:
        graph[a].append(b)       # a 是 b 的先修课：边 a -> b
        indegree[b] += 1
    pre = [0] * num_courses      # pre[v] 的第 u 位 = u 是 v 的先修
    queue = deque(i for i in range(num_courses)
                  if indegree[i] == 0)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            pre[v] |= pre[u] | (1 << u)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return [bool(pre[v] >> u & 1) for u, v in queries]
```

**复杂度。** 时间 `O(n·(n+E)/w + q)`，空间 `O(n²/w)`（`w` 为机器字长）。

**易错点。**
- 只看直接边：链 `0→1→2` 查 `[0,2]` 得 `False`，应为 `True`。
- 传播漏掉 `u` 自己：写成 `pre[v] |= pre[u]`，`pre[u]` 不含 `u`。
- 查询方向读反：要读 `pre[v]` 的第 `u` 位。

**追问。**
- 更直白的写法？：Floyd–Warshall，`reach[i][j] |= reach[i][k] and reach[k][j]`，`n=100` 只要 `10^6` 步。
- 图里可能有环？：先用强连通分量缩点，或直接用 Floyd–Warshall。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1334 阈值距离内邻居数最少的城市、LC 802 找到最终的安全状态
