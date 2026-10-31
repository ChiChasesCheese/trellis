---
id: tlc-parallel-courses-0-whole
node: c.parallel-courses
type: qa
---
## Q
**LC 1136 平行课程**｜Medium · LC TikTok 全时段热度 26/100

有 `n` 门课（编号 `1..n`）和先修关系 `relations`，`relations[i] = [prev, next]` 表示 `prev` 必须在 `next` 之前修完。一个学期可以修任意数量的课，前提是它们的先修课在**之前的学期**都已修完。返回修完所有课所需的最少学期数，若不可能返回 `-1`。`1 <= n <= 5000`，`1 <= relations.length <= 5000`，`prev != next`，所有 `[prev, next]` 互不相同。例：`n = 3, relations = [[1,3],[2,3]]` → `2`（第一学期修 1、2，第二学期修 3）；`n = 3, relations = [[1,2],[2,3],[3,1]]` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 拓扑排序按层进行（Kahn 算法）：每一层就是一个学期，入度为 0 的课同时修，层数就是学期数；修完的课少于 `n` 说明有环。

**识别。** 「先修关系」「最少轮数」：有向无环图上的拓扑分层，答案等于最长路径的节点数；有环则无解。

**推导。** 暴力：每个学期扫描所有课判断先修是否完成，`O(n * (n + E))`。洞察：用入度表代替扫描，一门课的入度降到 0 就意味着它的先修课全部完成，把这类课放进下一批；每一批对应一个学期。

```python
from collections import deque


def minimum_semesters(n: int, relations: list[list[int]]) -> int:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)                     # 每门课还剩几门先修课没修完
    for prev, nxt in relations:
        graph[prev].append(nxt)
        indegree[nxt] += 1

    ready = deque(c for c in range(1, n + 1) if indegree[c] == 0)   # 第一学期可修的课
    semesters = taken = 0
    while ready:
        semesters += 1
        for _ in range(len(ready)):              # 当前这一批课在同一学期修完
            course = ready.popleft()
            taken += 1
            for nxt in graph[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:           # 先修课全部修完，下一学期可修
                    ready.append(nxt)
    return semesters if taken == n else -1       # 有环则有课永远入度 > 0
```

运行：示例一 `2`；示例二 `-1`；`n = 1`、无关系 → `1`；`n = 4`、无关系 → `1`；链 `1 -> 2 -> 3 -> 4` → `4`。

**复杂度。** 时间 `O(n + E)`，空间 `O(n + E)`。

**拓展优化。**
- DFS 版本：沿「先修课」方向求最长链并检测环，`depth[c] = 1 + max(depth[pre])`。递归深度最坏为 `n`，`n = 5000` 超过 CPython 默认上限约 1000，需要提高递归上限：

```python
def minimum_semesters_dfs(n: int, relations: list[list[int]]) -> int:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for prev, nxt in relations:
        graph[nxt].append(prev)                  # 反向：指向先修课
    state = [0] * (n + 1)                        # 0 未访问，1 访问中，2 已完成
    depth = [0] * (n + 1)                        # depth[c]：修完 c 所需的最少学期数

    def dfs(c: int) -> bool:                     # 返回是否无环
        if state[c] == 1:
            return False                         # 回到访问中的节点：有环
        if state[c] == 2:
            return True
        state[c] = 1
        depth[c] = 1
        for pre in graph[c]:
            if not dfs(pre):
                return False
            depth[c] = max(depth[c], depth[pre] + 1)
        state[c] = 2
        return True

    if not all(dfs(c) for c in range(1, n + 1)):
        return -1
    return max(depth[1:])
```

**易错点。**
- 把每个节点出队时都 `semesters += 1`：同一批可并行修的课只计一个学期，要按批（`for _ in range(len(ready))`）计数。
- 不判断环：`[[1,2],[2,3],[3,1]]` 里没有入度为 0 的课，`ready` 为空，`semesters` 为 `0` 而不是 `-1`；必须核对 `taken == n`。
- 课程编号从 `1` 开始：邻接表和入度表要开 `n + 1`，否则下标越界或漏掉课程 `n`。

**追问。**
- 每学期最多修 `k` 门课（LC 1494 并行课程 II）：状态压缩 DP 或带优先级的贪心，不再是简单分层。
- 输出具体课表：BFS 时保存每一批的课程列表。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1494 并行课程 II、LC 310 最小高度树、LC 2050 并行课程 III。
