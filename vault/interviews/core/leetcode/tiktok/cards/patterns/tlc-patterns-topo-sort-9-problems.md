---
id: tlc-patterns-topo-sort-9-problems
node: patterns.topo-sort
type: qa
step: 9
---
## Q
**拓扑排序（Topological Sort）｜本组用到拓扑排序的题**

按变形分类，这个题组里哪些题属于拓扑排序？

## A
**判环与排序（课程表）**
- LC 207 课程表
- LC 210 课程表 II

**从偏序还原全序**
- LC 269 火星词典

**DAG 上的传递关系 / 动态规划**
- LC 1462 课程表 IV
- LC 329 矩阵中的最长递增路径

**相邻：图的方向与遍历**
- LC 1466 重新规划路线（树形图，遍历时统计需要改向的边）
- LC 399 除法求值（带权图）

提示：看到"先后顺序 / 依赖 / 能否全部完成"先画出"谁指向谁"，并写下 `[a, b]` 到底是 `a -> b` 还是 `b -> a`；再选 Kahn（分层、字典序、非递归）或 DFS 三色法。

**例题：** LC 207 课程表

共 `numCourses` 门课（`<= 2000`），`prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`，判断能否学完所有课程。

```python
from collections import deque
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
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
    return taken == num_courses
```

**例题：** LC 210 课程表 II

同上（`numCourses <= 2000`），返回一个能学完所有课程的学习顺序，有多个答案返回任意一个，学不完返回空数组。

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
        order.append(cur)
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

**例题：** LC 269 火星词典

给一组按某种外星字母顺序排好序的单词 `words`（`<= 100` 个，只含小写字母），返回一个与之一致的字母顺序，顺序自相矛盾则返回 `""`。

```python
from collections import deque
from itertools import pairwise
def alien_order(words: list[str]) -> str:
    graph: dict[str, set[str]] = {ch: set() for w in words for ch in w}
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    queue = deque(ch for ch, d in indeg.items() if d == 0)
    order: list[str] = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""
```

**例题：** LC 1462 课程表 IV

`numCourses` 门课（`<= 100`）的先修关系构成无环图，先修可以是间接的；对每个查询 `[u, v]`（最多 `10^4` 个）回答 `u` 是否是 `v` 的（直接或间接）先修课。

```python
from collections import deque
def check_if_prerequisite(num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        graph[a].append(b)
        indegree[b] += 1
    pre = [0] * num_courses
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            pre[v] |= pre[u] | (1 << u)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return [bool(pre[v] >> u & 1) for u, v in queries]
```

**例题：** LC 329 矩阵中的最长递增路径

给整数矩阵（`m, n <= 200`），求沿上下左右移动、数值严格递增的最长路径的长度。

```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]
    def dfs(i: int, j: int) -> int:
        if memo[i][j]:
            return memo[i][j]
        best = 1
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))
        memo[i][j] = best
        return best
    return max(dfs(i, j) for i in range(m) for j in range(n))
```

**例题：** LC 1466 重新规划路线

`n` 座城市（`n <= 5 * 10^4`）由 `n - 1` 条有向道路连成一棵树，求最少反转多少条道路的方向，才能让所有城市都能到达城市 `0`。

```python
def min_reorder(n: int, connections: list[list[int]]) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))
        adj[b].append((a, 0))
    def dfs(u: int, parent: int) -> int:
        flips = 0
        for v, cost in adj[u]:
            if v != parent:
                flips += cost + dfs(v, u)
        return flips
    return dfs(0, -1)
```

**例题：** LC 399 除法求值

给已知等式 `Ai / Bi = values[i]`（最多 `20` 条，`0 < values[i] <= 20`）和若干查询 `Cj / Dj`，返回每个查询的值；无法确定或变量未出现时为 `-1.0`。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}
    def find(x: str) -> str:
        p = parent.setdefault(x, x)
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)
            ratio[x] *= ratio[p]
            parent[x] = root
        return parent[x]
    for (a, b), v in zip(equations, values):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            ratio[ra] = v * ratio[b] / ratio[a]
    ans: list[float] = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])
        else:
            ans.append(-1.0)
    return ans
```
