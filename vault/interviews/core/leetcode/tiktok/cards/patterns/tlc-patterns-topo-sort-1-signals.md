---
id: tlc-patterns-topo-sort-1-signals
node: patterns.topo-sort
type: qa
step: 1
---
## Q
**拓扑排序（Topological Sort）｜信号**

什么样的题面该想到拓扑排序？Kahn 算法和 DFS 三色法分别适合什么场景？

## A
**触发信号：**
- 事物之间有**先后依赖**：先修课程、任务前置、编译顺序（LC 207、210、1462）（例：LC 207 课程表）。
- 问「能否全部完成」= **有向图是否有环**（LC 207）（例：检测循环依赖）。
- 要「输出一个合法顺序」（LC 210）（例：LC 210 课程表 II）。
- 从**元素之间的偏序**还原全序：火星词典（LC 269），相邻单词的第一个不同字母给出一条边（例：LC 269 火星词典）。
- 「最长递增路径」这类**在 DAG 上做 DP**，按拓扑顺序（或记忆化）计算（LC 329）（例：LC 329 矩阵中的最长递增路径）。
- 「分层 / 最少几轮」：每一轮取出所有入度为 0 的点（并行学期数）（例：LC 2050 并行课程 III）。

**两种实现：**
- **Kahn 算法**（BFS，入度表）：反复取出入度为 0 的点；`O(V + E)`；环的判定很自然：取出的点数 `< V`（例：LC 1462 课程表 IV）。
- **DFS 三色法**（0 未访问 / 1 在当前路径 / 2 已完成）：遇到状态 1 的点即有环；完成时入列表，反转得到拓扑序（例：LC 332 重新安排行程）。

**怎么选**：要分层、要字典序最小（改用堆）、要避免递归 → Kahn；写起来更短或要在 DFS 里顺便做计算 → DFS。

**近似信号：**
- 无向图的环 → 并查集或 DFS 记父节点，不是拓扑排序（例：LC 1319 连通网络的操作次数；高频：LC 323 无向图中连通分量的数目）。
- 图本身有环但问最短路 → Dijkstra / BFS（例：LC 787 K 站中转内最便宜的航班）。
- 只需要判断两点是否连通 → BFS / 并查集（例：LC 547 省份数量；高频：LC 200 岛屿数量）。
- 数据范围：`numCourses <= 2000`、边 `<= 5000` 这类，`O(V + E)` 绰绰有余（例：LC 207 课程表）。

**例题：** LC 207 课程表

共 `numCourses` 门课（`1 <= numCourses <= 2000`），`prerequisites[i] = [a, b]`（至多 5000 对）表示学 `a` 之前必须先学 `b`，判断能否学完所有课程。

```python
from collections import deque
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)                  # 边 pre -> course：先修课指向后修课
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses                    # 有环 => 环上的点入度永远降不到 0
```

**例题：** 检测循环依赖

`n` 个模块（`1 <= n <= 10^5`），`deps[k] = [a, b]` 表示 `a` 依赖 `b`（至多 `2 * 10^5` 条，可重复），判断依赖里是否存在循环依赖。

```python
from collections import deque
def has_cycle(n: int, deps: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:                       # a 依赖 b：先有 b 才能有 a，边 b -> a
        graph[b].append(a)
        indeg[a] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)   # 没有任何前置依赖的模块先上
    done = 0
    while queue:
        u = queue.popleft()
        done += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return done < n                         # 有模块始终入度不为 0：它们在环上或依赖环上的模块
```

**例题：** LC 210 课程表 II

共 `numCourses` 门课（`1 <= numCourses <= 2000`），`prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`，返回一种可行的学习顺序，有环返回空数组。

```python
from collections import deque
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order: list[int] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)                          # 出队顺序就是一个合法的拓扑序
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

**例题：** LC 269 火星词典

一种未知字母顺序的语言，`words`（`1 <= words.length <= 100`，每个词长 `1..100`，小写字母）已按该语言字典序排好。还原一个合法的字母顺序，矛盾则返回 `""`。

```python
from collections import deque
from itertools import pairwise
def alien_order(words: list[str]) -> str:
    graph: dict[str, set[str]] = {ch: set() for w in words for ch in w}   # 出现过的每个字母都是结点
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):                 # 只有相邻两个词能提供约束
        for x, y in zip(a, b):
            if x != y:                           # 第一个不同的字母：x 排在 y 前面
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):                  # b 是 a 的真前缀却排在后面：非法
                return ""
    queue = deque(ch for ch, d in indeg.items() if d == 0)
    order: list[str] = []
    while queue:                                 # Kahn 拓扑排序
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""   # 没排完说明有环
```

**例题：** LC 329 矩阵中的最长递增路径

`m x n` 整数矩阵（`1 <= m, n <= 200`），可向上下左右移动，求严格递增路径的最大长度。

```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]         # memo[i][j]：从 (i, j) 出发的最长递增路径点数，0 表示还没算
    def dfs(i: int, j: int) -> int:
        if memo[i][j]:
            return memo[i][j]
        best = 1                               # 至少有自己
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))   # 邻居严格更大才能走，所以不会走回头路
        memo[i][j] = best
        return best
    return max(dfs(i, j) for i in range(m) for j in range(n))
```

**例题：** LC 2050 并行课程 III

`n` 门课（`1 <= n <= 5 * 10^4`），`relations[j] = [prev, next]` 表示 `prev` 必须先于 `next`，`time[i]` 是第 `i+1` 门课所需月数；可同时上任意多门课，先修课全部完成后即可开始，求学完所有课的最少月数（保证无环）。

```python
from collections import deque
def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for before, after in relations:
        graph[before - 1].append(after - 1)
        indegree[after - 1] += 1
    finish = time.copy()
    queue = deque(i for i in range(n) if indegree[i] == 0)
    while queue:
        course = queue.popleft()
        for nxt in graph[course]:
            finish[nxt] = max(finish[nxt], finish[course] + time[nxt])
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return max(finish)
```

**例题：** LC 1462 课程表 IV

`numCourses` 门课（`2 <= numCourses <= 100`，先修关系无环），`prerequisites[i] = [a, b]` 表示 `a` 是 `b` 的先修课（可以是间接先修），回答一批 `queries[j] = [u, v]`：`u` 是否是 `v` 的先修课。

```python
from collections import deque
def check_if_prerequisite(num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:             # a 是 b 的先修课：边 a -> b
        graph[a].append(b)
        indegree[b] += 1
    pre = [0] * num_courses                # pre[v]：位集，第 u 位为 1 表示 u 是 v 的（直接或间接）先修课
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    while queue:                           # 拓扑序：处理 u 时，它的所有先修课都已并入 pre[u]
        u = queue.popleft()
        for v in graph[u]:
            pre[v] |= pre[u] | (1 << u)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return [bool(pre[v] >> u & 1) for u, v in queries]
```

**例题：** LC 332 重新安排行程

机票列表 `tickets[i] = [from, to]`（`1 <= tickets.length <= 300`，机场名为 3 个大写字母），所有行程从 `"JFK"` 出发，每张票恰好用一次，返回字典序最小的合法行程。

```python
def find_itinerary(tickets: list[list[str]]) -> list[str]:
    graph = {}
    for a, b in sorted(tickets, reverse=True):            # 逆序排序，pop() 取到字典序最小的目的地
        graph.setdefault(a, []).append(b)
    stack, route = ["JFK"], []
    while stack:
        while graph.get(stack[-1]):                       # 一路走到走不动为止
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                         # 走不动的机场排在剩余行程的最后
    return route[::-1]
```

**例题：** LC 1319 连通网络的操作次数

`n` 台计算机（`1 <= n <= 10^5`）由无向网线 `connections`（至多 `10^5` 条）相连；一次操作可拔下一条现有网线，重新接到两台尚未相连的计算机上。求让整个网络连通的最少操作数，不可能则 `-1`。

```python
def make_connected(n: int, connections: list[list[int]]) -> int:
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))
    components = n
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            components -= 1
    return components - 1
```

**例题：** LC 787 K 站中转内最便宜的航班

`n` 个城市（`2 <= n <= 100`），`flights[i] = [from, to, price]`（`1 <= price <= 10^4`），求从 `src` 到 `dst`、最多经过 `k` 站中转的最低价格，没有则 `-1`。

```python
from math import inf
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0                          # 0 趟航班：只在出发地，价格 0
    for t in range(1, k + 2):               # 最多 k 个中转 = 最多 k + 1 趟航班
        dp[t] = dp[t - 1][:]                # 少坐一趟也算（"最多 t 趟"）
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:  # 只读上一行：这一行多坐的恰好一趟
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

**例题：** LC 547 省份数量

`n x n` 邻接矩阵 `isConnected`（`1 <= n <= 200`，对称，对角线为 1），`isConnected[i][j] = 1` 表示城市 `i`、`j` 直接相连；直接或间接相连的城市构成一个省份，求省份总数。

```python
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # 路径减半
            x = parent[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                root_i, root_j = find(i), find(j)
                if root_i != root_j:
                    parent[root_i] = root_j
    return len({find(i) for i in range(n)})
```

**例题：** LC 323 无向图中连通分量的数目

无向图有 `n` 个节点，下标 `0` 到 `n - 1`；`edges[i] = [a, b]` 表示 `a` 与 `b` 之间有一条边。返回图中**连通分量**（互相可达的一组节点）的个数。`1 <= n <= 2000`，`1 <= edges.length <= 5000`，`0 <= a <= b < n`，`a != b`，没有重复的边。

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径减半：顺手把 x 挂到祖父下面
            x = parent[x]
        return x

    comps = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:                           # 两端本来不连通：合并一次，分量少一个
            parent[ra] = rb
            comps -= 1
    return comps
```

**例题：** LC 200 岛屿数量

给一个由 `'1'`（陆地）和 `'0'`（水）组成的二维网格 `grid`，数其中岛屿的数量。岛屿由水平或竖直方向相邻的陆地连成，四条边外面都是水。`m == grid.length`，`n == grid[i].length`，`1 <= m, n <= 300`，`grid[i][j]` 是 `'0'` 或 `'1'`。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return                                      # 出界或水：这条搜索到头
        grid[r][c] = "0"                                # 先沉掉再往四周搜，同一格不会被重复进入
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                              # 找到一座新岛：把它整座沉掉
                sink(r, c)
    return count
```
