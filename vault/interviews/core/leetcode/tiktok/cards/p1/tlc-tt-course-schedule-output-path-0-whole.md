---
id: tlc-tt-course-schedule-output-path-0-whole
node: p1.tt-course-schedule-output-path
type: qa
---
## Q
**课程表输出学习顺序，及单词接龙输出最短路径**｜Medium · 近一年被问：美国 15 次、国内 4 次 · 最近 2026-10-15（面试记录）

同一场面试的两问。第一问：`numCourses` 门课（编号 `0` 到 `numCourses - 1`）和先修关系 `prerequisites`，`[a, b]` 表示学 `a` 之前必须先学 `b`；判断能否学完全部课程，能就**输出一种可行的学习顺序**，不能返回空列表。`1 <= numCourses <= 2000`，`0 <= len(prerequisites) <= 5000`，关系互不相同。第二问：给 `begin`、`end` 和单词列表 `words`（长度相同，全小写，`1 <= len(words) <= 5000`，单词长度 `<= 10`，`begin != end`），每次只能改一个字母且结果必须在 `words` 里，输出一条从 `begin` 到 `end` 的**最短转换路径**（含首尾），不可达返回空列表。例：`(4, [[1,0],[2,0],[3,1],[3,2]])` → `[0, 1, 2, 3]`；`("hit", "cog", ["hot","dot","dog","lot","log","cog"])` → `['hit','hot','dot','dog','cog']`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两问都是图上的 BFS。第一问用入度的拓扑排序（Kahn 算法）：入度为 `0` 的课先学，学完把后继课的入度减 `1`，减到 `0` 入队；出队顺序就是学习顺序，若出队数少于课程数说明有环。第二问在“只差一个字母”的图上做 BFS，用通配模式（`h*t`）分桶找邻居，并在入队时记前驱，到达 `end` 后沿前驱回溯再反转。

**识别。** 「先修关系」是有向图，「能否学完」是判环，「输出顺序」是拓扑序。「每步改一个字母、最少步数」是无权图的最短路，BFS；「输出路径」就是多记一个前驱指针。两问共同的套路：BFS 的“已访问”表与“前驱”表可以是同一个。

**推导。** 第一问暴力：每次扫全部课程找“先修都已学完”的，`O(V · (V + E))`。浪费：每轮重复检查。洞察：维护入度，学完一门课只更新它的后继，每条边处理一次，`O(V + E)`。第二问暴力：对每个单词两两比较是否只差一个字母，`O(N^2 · L)`，`N = 5000` 要 `10^8` 以上次字符比较。洞察：把每个单词的每个位置替换成 `*`，得到 `L` 个模式，同一个模式下的单词互为邻居，建桶后每个单词只需看 `L` 个桶，`O(N · L^2)`。

```python
from collections import defaultdict, deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """prerequisites[i] = [a, b]：学 a 之前必须先学 b。返回一种可行学习顺序；有环返回 []。"""
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)                 # 边 pre -> course
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order: list[int] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []     # 有环时总有节点入度永远不为 0


def shortest_ladder(begin: str, end: str, words: list[str]) -> list[str]:
    """每次改一个字母，且结果必须在 words 里。返回一条最短转换路径（含首尾），不可达返回 []。"""
    if end not in set(words):
        return []
    buckets: defaultdict[str, list[str]] = defaultdict(list)    # 通配模式 -> 单词，如 "h*t" -> [hot, hit]
    for w in dict.fromkeys((begin, *words)):
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    parent: dict[str, str | None] = {begin: None}               # 既是 visited，又记前驱
    queue = deque([begin])
    while queue:
        cur = queue.popleft()
        if cur == end:
            break
        for i in range(len(cur)):
            for nxt in buckets[cur[:i] + "*" + cur[i + 1:]]:
                if nxt not in parent:
                    parent[nxt] = cur
                    queue.append(nxt)
    if end not in parent:
        return []
    path: list[str] = []
    node: str | None = end
    while node is not None:                                     # 顺着前驱回溯，再反转
        path.append(node)
        node = parent[node]
    return path[::-1]
```

运行：`find_order(4, [[1,0],[2,0],[3,1],[3,2]])` → `[0, 1, 2, 3]`，`find_order(2, [[1,0],[0,1]])` → `[]`，`find_order(1, [])` → `[0]`，`n = 2000` 的一条链 → 正常；`shortest_ladder("hit", "cog", [...])` → `['hit', 'hot', 'dot', 'dog', 'cog']`，`words` 里没有 `"cog"` → `[]`。

**复杂度。** 课程：时间 `O(V + E)`，空间 `O(V + E)`。接龙：建桶 `O(N · L^2)`（每个单词 `L` 个模式，每个模式切片 `O(L)`），BFS 同阶，空间 `O(N · L)`。

**易错点。**
- 边的方向反了：`[a, b]` 是 `b` 在前，边应是 `b -> a`。写成 `graph[a].append(b)`，`(2, [[1,0]])` 得到 `[1, 0]`，正确是 `[0, 1]`。
- 不检查出队数量：有环时仍返回已排出的部分。`(3, [[1,2],[2,1]])`（课程 `1`、`2` 互相依赖）返回 `[0]`，正确是 `[]`。
- 单词接龙要在**入队时**记前驱并标记已访问，否则同一个单词被多次入队，路径可能被后来者覆盖、队列膨胀。
- `end` 不在 `words` 里要直接返回空列表；两两比较单词建图在 `N = 5000` 时超时，必须分桶。

**追问。**
- 字典序最小的课程顺序：把 `deque` 换成 `heapq` 最小堆，每次取编号最小的可学课程；`(3, [[0,2],[1,2]])` → `[2, 0, 1]`。
- 并行学习，每门课有时长（Parallel Courses III）：沿拓扑序做 DP，`done[v] = 自身时长 + max(先修的 done)`，答案取最大值。
- 输出**所有**最短接龙路径：BFS 记录每个单词的所有前驱（只在距离恰好小一层时），到达后 DFS 回溯展开。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 127 单词接龙、LC 126 单词接龙 II、LC 2050 并行课程 III、LC 1136 并行课程。
