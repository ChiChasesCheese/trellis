---
id: tlc-course-schedule-4-followup
node: p1.course-schedule
type: qa
step: 4
---
## Q
**LC 207 课程表**｜追问

面试官接着问：（1）每学期可以同时学任意多门，最少几个学期学完？（2）用 DFS 怎么判环，在 2000 门课串成链时会遇到什么问题？（3）要输出一个具体的学习顺序呢？

## A
1. **最少学期数**：Kahn 按层处理，每一层是同一学期能学的课。有环返回 `-1`。

```python
def minimum_semesters(n: int, prerequisites: list[list[int]]) -> int:
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    layer = [i for i, d in enumerate(indegree) if d == 0]
    semesters = taken = 0
    while layer:
        semesters += 1
        taken += len(layer)
        next_layer = []
        for cur in layer:
            for nxt in graph[cur]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    next_layer.append(nxt)
        layer = next_layer
    return semesters if taken == n else -1
```

`minimum_semesters(3, [[1,0],[2,0]])` → `2`，`minimum_semesters(3, [[1,2],[2,1]])` → `-1`。学期数等于图里最长链的点数。
2. **DFS 三色标记**：状态 `0` 未访问、`1` 在当前路径上、`2` 已完成；遇到状态 `1` 的点就是环。

```python
def can_finish_dfs(n: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n)]
    for course, pre in prerequisites:
        graph[pre].append(course)
    state = [0] * n

    def dfs(u: int) -> bool:
        state[u] = 1
        for v in graph[u]:
            if state[v] == 1 or (state[v] == 0 and not dfs(v)):
                return False
        state[u] = 2
        return True

    return all(state[u] == 2 or dfs(u) for u in range(n))
```

`2000` 门课串成一条从 `0` 开始的链时，递归深度到 2000，超过默认上限 1000，抛出 `RecursionError`；要么改成显式栈，要么直接用 Kahn。
3. **输出顺序**：Kahn 里把出队的课程依次记下来就是一个合法顺序，这正是 LC 210。

**Python 提醒**：`all(state[u] == 2 or dfs(u) for u in range(n))` 依赖生成器的短路，某个 `dfs` 返回 `False` 就立刻停止；不要把它改成先建列表再 `all`，那样会无谓地跑完所有起点。
