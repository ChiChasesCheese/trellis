---
slug: parallel-courses-iii
---
## Q
**LC 2050 并行课程 III**｜Hard

`n` 门课，`relations` 给出先修关系（DAG），`time[i]` 是第 `i+1` 门课所需月数；先修课全修完即可开始，可同时修任意多门。求修完所有课的最少月数。

## A
**一句话。** 拓扑排序 + DP：最早开始时间取所有先修课完成时间的最大值，答案是最大完成时间。

```python
def minimum_time(n, relations, time):
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        g[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)      # 最早开始月份
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    ans = 0
    while q:
        u = q.popleft()
        fin = start[u] + time[u - 1]
        ans = max(ans, fin)
        for v in g[u]:
            start[v] = max(start[v], fin)   # 要等所有先修课
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ans
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`。

**易错点。**
- 答案取最后出队那门课的完成时间：`n=3`, 无先修, `time=[1,9,4]` 得 `4`，应为 `9`。
- 后继开始时间不取最大值而是覆盖：示例二得 `7`，应为 `12`。
- 把所有课时间相加：忽略并行，示例一得 `10`，应为 `8`。

**追问。**
- 怎么输出关键路径？：更新 `start[v]` 变大时记 `prev[v] = u`，从完成最晚的课回溯。
- 输入可能有环？：出队的课程数小于 `n` 就说明有环。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1136 并行课程、LC 1857 有向图中最大颜色值
