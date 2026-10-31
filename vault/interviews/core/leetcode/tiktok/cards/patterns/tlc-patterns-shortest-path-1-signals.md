---
id: tlc-patterns-shortest-path-1-signals
node: patterns.shortest-path
type: qa
step: 1
---
## Q
**最短路（Shortest Path）｜信号**

什么样的题面该想到 Dijkstra、Bellman-Ford、0-1 BFS，还是普通 BFS？"带状态的最短路"怎么识别？

## A
先看**边的代价**：

| 边的代价 | 算法 | 复杂度 |
|---|---|---|
| 每步代价相同（或只数步数） | BFS | `O(V + E)` |
| 只有 0 和 1 | 0-1 BFS（双端队列） | `O(V + E)` |
| 非负且不全相同 | Dijkstra（最小堆） | `O((V + E) log V)` |
| 有负权，或**限制经过的边数** | Bellman-Ford | `O(k · E)` |
| 所有点对 | Floyd | `O(V^3)`，`V <= 100` |

**触发信号：**
- 「最短 / 最少花费」且各条边的代价不同、都非负：用最小堆，每次取出当前最小代价的点（例：LC 778 水位上升的泳池中游泳）。
- 「**最多经过 `k` 站**」「最多 `k` 条边」：限制边数 ⇒ Bellman-Ford 按轮松弛，或把"已用边数"放进状态（例：LC 787 K 站中转内最便宜的航班）。
- 网格里**可以消除 `k` 个障碍**：状态不只是位置，还有"剩余次数"：`(r, c, left)`，在状态图上做 BFS（例：LC 1293 网格中的最短路径）。
- 状态之间的转移代价相同，但状态里带着额外信息 ⇒ 在 `(点, 状态)` 上做普通 BFS（例：LC 1293 网格中的最短路径）。

**近似信号：**
- 只问连通性 ⇒ 并查集 / DFS（例：LC 721 账户合并）。
- 无权图用 Dijkstra 也对，但 BFS 更简单更快（例：LC 542 01 矩阵；高频：LC 1091 二进制矩阵中的最短路径）。
- 有负权环时最短路无定义；Dijkstra 在有负权边时可能出错，有负权就用 Bellman-Ford（例：LC 787 K 站中转内最便宜的航班）。
- 要最小生成树（连通所有点的最小总边权）⇒ Kruskal / Prim，不是最短路（例：LC 1584 连接所有点的最小费用）。
- 数据范围 `n <= 100`，且要问任意两点是否可达或距离 ⇒ `O(n^3)` 的 Floyd 传递闭包也可行（例：LC 399 除法求值）。

**例题：** LC 787 K 站中转内最便宜的航班

`n` 个城市和带价格的航班，求从 `src` 到 `dst` 最多中转 `k` 站的最便宜价格，不存在返回 `-1`，`2 <= n <= 100`，`1 <= price <= 10^4`。

```python
from math import inf
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0
    for t in range(1, k + 2):
        dp[t] = dp[t - 1][:]
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

**例题：** LC 1293 网格中的最短路径

`m x n` 网格，`0` 是空、`1` 是障碍，最多可以消除 `k` 个障碍，求从左上角到右下角的最短步数，找不到返回 `-1`，`1 <= m, n <= 40`。

```python
from collections import deque
def shortest_path(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if k >= m + n - 3:
        return m + n - 2
    best_left = [[-1] * n for _ in range(m)]
    best_left[0][0] = k
    queue = deque([(0, 0, k)])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):
            i, j, left = queue.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if not (0 <= ni < m and 0 <= nj < n):
                    continue
                nleft = left - grid[ni][nj]
                if nleft > best_left[ni][nj]:
                    if (ni, nj) == (m - 1, n - 1):
                        return steps
                    best_left[ni][nj] = nleft
                    queue.append((ni, nj, nleft))
    return -1
```

**例题：** LC 721 账户合并

每个账户是名称加若干邮箱，只要有共同邮箱就是同一个人，合并后每个账户的邮箱按字典序排好，`1 <= accounts.length <= 1000`。

```python
from collections import defaultdict
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    parent = list(range(len(accounts)))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    owner: dict[str, int] = {}
    for i, (_, *emails) in enumerate(accounts):
        for email in emails:
            j = owner.setdefault(email, i)
            if j != i:
                parent[find(i)] = find(j)
    groups: defaultdict[int, list[str]] = defaultdict(list)
    for email, i in owner.items():
        groups[find(i)].append(email)
    return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]
```

**例题：** LC 542 01 矩阵

返回同样大小的矩阵，每个格子是 `mat` 中该位置到最近的 `0` 的距离（相邻距离为 1），`1 <= m * n <= 10^4`，至少有一个 `0`。

```python
from collections import deque
from itertools import pairwise
def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    queue: deque[tuple[int, int]] = deque()
    for i, row in enumerate(mat):
        for j, value in enumerate(row):
            if value == 0:
                dist[i][j] = 0
                queue.append((i, j))
    while queue:
        i, j = queue.popleft()
        for di, dj in pairwise((1, 0, -1, 0, 1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] == -1:
                dist[ni][nj] = dist[i][j] + 1
                queue.append((ni, nj))
    return dist
```

**例题：** LC 1584 连接所有点的最小费用

平面上的点两两连线的费用是曼哈顿距离，求让所有点连通（任意两点恰有一条简单路径）的最小总费用，`1 <= points.length <= 1000`。

```python
def min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    INF = 1 << 60
    dist = [INF] * n
    dist[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=dist.__getitem__)
        used[u] = True
        total += dist[u]
        ux, uy = points[u]
        for v in range(n):
            if not used[v]:
                d = abs(ux - points[v][0]) + abs(uy - points[v][1])
                if d < dist[v]:
                    dist[v] = d
    return total
```

**例题：** LC 399 除法求值（Floyd 写法）

给已知等式 `Ai / Bi = values[i]`（`1 <= equations.length <= 20`，`0.0 < values[i] <= 20.0`，变量名长度 `<= 5`）和若干查询 `Cj / Dj`（最多 `20` 个），返回每个查询的值；无法确定或变量没出现过时为 `-1.0`。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    names = sorted({v for pair in equations for v in pair})
    idx = {v: i for i, v in enumerate(names)}
    n = len(names)
    ratio = [[0.0] * n for _ in range(n)]            # ratio[i][j]：i / j，0.0 表示还不知道
    for i in range(n):
        ratio[i][i] = 1.0
    for (a, b), v in zip(equations, values):
        ratio[idx[a]][idx[b]] = v
        ratio[idx[b]][idx[a]] = 1 / v
    for k in range(n):                               # Floyd：经过 k 中转，i / j = (i / k) * (k / j)
        for i in range(n):
            if ratio[i][k]:
                for j in range(n):
                    if ratio[k][j] and not ratio[i][j]:
                        ratio[i][j] = ratio[i][k] * ratio[k][j]
    ans: list[float] = []
    for c, d in queries:
        r = ratio[idx[c]][idx[d]] if c in idx and d in idx else 0.0
        ans.append(r or -1.0)
    return ans
```

**例题：** LC 778 水位上升的泳池中游泳

`n x n` 矩阵 `grid[i][j]` 是平台高度，时刻 `t` 的水位是 `t`，只有水位不低于相邻两平台的高度时才能游过去；返回从 `(0, 0)` 到 `(n-1, n-1)` 的最少时间；`1 <= n <= 50`，高度互不相同。

```python
from heapq import heappop, heappush
def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)
        if x == y == n - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                seen.add((nx, ny))
                heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return -1
```

**例题：** LC 1091 二进制矩阵中的最短路径

`n x n` 的 0/1 矩阵，从左上角走到右下角，只能走值为 `0` 的格子，八个方向都可以走，返回最短路径经过的格子数，不存在返回 `-1`；`1 <= n <= 100`。

```python
from collections import deque
from itertools import product
def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    dirs = [(dr, dc) for dr, dc in product((-1, 0, 1), repeat=2) if dr or dc]
    seen = [row[:] for row in grid]
    seen[0][0] = 1
    q = deque([(0, 0, 1)])
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = 1
                q.append((nr, nc, d + 1))
    return -1
```
