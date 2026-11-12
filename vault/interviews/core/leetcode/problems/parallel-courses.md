---
slug: parallel-courses
---
## Q
**LC 1136 平行课程**｜Medium

`n` 门课有先修关系，一学期可修任意多门先修课已在之前学期修完的课。求最少学期数，有环返回 `-1`。

## A
**一句话。** 按层的拓扑排序（Kahn）：每一层入度为 0 的课就是一个学期，修完的课数不足 `n` 说明有环。

```python
def minimum_semesters(n, relations):
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for p, c in relations:
        g[p].append(c)
        indeg[c] += 1
    q = deque(c for c in range(1, n + 1) if indeg[c] == 0)
    sem = taken = 0
    while q:
        sem += 1
        for _ in range(len(q)):    # 同一批在一个学期修完
            u = q.popleft()
            taken += 1
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
    return sem if taken == n else -1
```

**复杂度。** 时间 `O(n + E)`，空间 `O(n + E)`。

**易错点。**
- 每个节点出队都 `sem += 1`：同一批可并行修，按层计一个学期。
- 不判环：`[[1,2],[2,3],[3,1]]` 没有入度为 `0` 的课，会返回 `0`，要核对 `taken == n`。

**追问。**
- 每学期最多修 `k` 门（LC 1494）？：状态压缩 DP，不再是简单分层。
- 要输出具体课表？：BFS 时保存每一批的课程列表。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 2050 并行课程 III、LC 1494 并行课程 II
