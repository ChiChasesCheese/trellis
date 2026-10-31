---
id: tlc-patterns-shortest-path-7-problems
node: patterns.shortest-path
type: qa
step: 7
---
## Q
**最短路（Shortest Path）｜本组用到最短路的题**

按变形分类，这个题组里哪些题属于最短路？

## A
**加权图 / 限制边数**
- LC 787 K 站中转内最便宜的航班（Bellman-Ford，或 Dijkstra 加站数状态）
- LC 399 除法求值（图上的路径乘积，可用 DFS / 带权并查集）
- LC 778 水位上升的泳池中游泳（高频）

**带状态的 BFS**
- LC 1293 网格中的最短路径（状态含剩余消除次数）
- 带油量限制和补给点的网格最小代价路径（高频）

**无权最短路（BFS）**
- LC 127 单词接龙
- LC 815 公交路线
- LC 994 腐烂的橘子（多源）
- LC 286 墙与门（多源）
- LC 1091 二进制矩阵中的最短路径（高频）
- 量水问题：最短操作序列（高频）

**相邻：最小生成树**
- LC 1584 连接所有点的最小费用（Kruskal）

提示：先看边的代价，再看有没有"最多 `k` 步 / 最多消除 `k` 次"这类限制，限制就是状态的一个分量。

**例题：** LC 787 K 站中转内最便宜的航班

`n` 个城市（`n <= 100`）和带价格的有向航班，求从 `src` 到 `dst` 最多经过 `k` 次中转的最便宜价格，不存在返回 `-1`。

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

**例题：** LC 1293 网格中的最短路径

`m x n` 的 0/1 网格（`m, n <= 40`，`1` 为障碍），最多可以消除 `k` 个障碍，求从左上角走到右下角（上下左右）的最少步数，走不到返回 `-1`。

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

**例题：** LC 127 单词接龙

给 `beginWord`、`endWord` 和字典 `wordList`（最多 `5000` 个、等长小写单词），每步只改一个字母且结果必须在字典里，求最短转换序列的单词数，不存在返回 `0`。

```python
import string
from collections import deque
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    queue = deque([begin_word])
    steps = 1
    while queue:
        for _ in range(len(queue)):
            word = queue.popleft()
            if word == end_word:
                return steps
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words:
                        words.remove(nxt)
                        queue.append(nxt)
        steps += 1
    return 0
```

**例题：** LC 815 公交路线

`routes[i]` 是第 `i` 条循环公交线路经过的车站（`routes.length <= 500`，站点总数 `<= 10^5`）；从 `source` 站出发去 `target` 站，只能乘公交，求最少乘坐的公交车数，到不了返回 `-1`。

```python
from collections import defaultdict, deque
def num_buses_to_destination(routes: list[list[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    stop_routes: defaultdict[int, list[int]] = defaultdict(list)
    for r, stops in enumerate(routes):
        for stop in stops:
            stop_routes[stop].append(r)
    seen_stops = {source}
    seen_routes: set[int] = set()
    queue = deque([source])
    buses = 0
    while queue:
        buses += 1
        for _ in range(len(queue)):
            stop = queue.popleft()
            for r in stop_routes.get(stop, ()):
                if r in seen_routes:
                    continue
                seen_routes.add(r)
                for nxt in routes[r]:
                    if nxt == target:
                        return buses
                    if nxt not in seen_stops:
                        seen_stops.add(nxt)
                        queue.append(nxt)
    return -1
```

**例题：** LC 994 腐烂的橘子

网格（`m, n <= 10`）中 `0` 空、`1` 新鲜橘子、`2` 腐烂橘子，每分钟腐烂橘子使上下左右的新鲜橘子腐烂；求所有橘子腐烂所需的最少分钟数，做不到返回 `-1`。

```python
from collections import deque
def oranges_rotting(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    queue = deque((i, j) for i, row in enumerate(grid) for j, v in enumerate(row) if v == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            i, j = queue.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2
                    fresh -= 1
                    queue.append((ni, nj))
    return -1 if fresh else minutes
```

**例题：** LC 286 墙与门

`m x n` 网格（`m, n <= 250`）中 `-1` 是墙，`0` 是门，`INF = 2147483647` 是空房间；原地把每个空房间填成到最近的门的步数（上下左右），到不了则保持 `INF`。

```python
from collections import deque
INF = 2**31 - 1
def walls_and_gates(rooms: list[list[int]]) -> None:
    m, n = len(rooms), len(rooms[0])
    queue = deque((r, c) for r in range(m) for c in range(n) if rooms[r][c] == 0)
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

**例题：** LC 1584 连接所有点的最小费用

给二维平面上的 `points`（`<= 1000` 个点），连接两点的费用是曼哈顿距离，求使所有点连通的最小总费用。

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

**例题：** LC 778 水位上升的泳池中游泳

`n x n` 的整数矩阵 `grid`，`grid[i][j]` 是位置 `(i, j)` 平台的高度。时间为 `t` 时水位是 `t`。你可以从一个平台游向上下左右相邻的平台，前提是此时水位**同时淹没**这两个平台（`t` 不小于两者的高度）；在平台内部移动、瞬间移动都不耗时。你从左上角 `(0, 0)` 出发，返回到达右下角 `(n-1, n-1)` 所需的**最少时间**。`1 <= n <= 50`，`0 <= grid[i][j] < n^2`，所有高度互不相同。

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

**例题：** 带油量限制和补给点的网格最小代价路径

`m x n` 的网格 `grid`：`grid[r][c] >= 0` 是进入该格的代价，`-1` 是障碍不能走；另有一组补给点 `recharge`，到达补给点后油量立刻恢复到满（`K`）。起点 `(0, 0)`（不计入场代价），终点 `(m-1, n-1)`，初始油量为 `K`，每向上下左右走一步消耗 `1` 单位油，油量为 `0` 时不能再走。求从起点到终点的最小总代价，不可达返回 `-1`。`1 <= m, n <= 50`，`0 <= grid[r][c] <= 100`（障碍除外），`0 <= K <= 10^9`。

```python
import heapq
def min_cost(grid: list[list[int]], recharge: set[tuple[int, int]], fuel: int) -> int:
    """grid[r][c] 是进入该格的代价，-1 表示障碍；到达 recharge 里的格子油量恢复到 fuel；每走一步耗 1 单位油。
    从 (0, 0) 到 (m-1, n-1) 的最小总代价，不可达返回 -1。"""
    m, n = len(grid), len(grid[0])
    if grid[0][0] == -1 or grid[m - 1][n - 1] == -1:
        return -1
    fuel = min(fuel, m * n)
    best_fuel = [[-1] * n for _ in range(m)]
    heap = [(0, 0, 0, fuel)]
    while heap:
        cost, r, c, left = heapq.heappop(heap)
        if (r, c) == (m - 1, n - 1):
            return cost
        if left <= best_fuel[r][c]:
            continue
        best_fuel[r][c] = left
        if left == 0:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
                nxt_fuel = fuel if (nr, nc) in recharge else left - 1
                heapq.heappush(heap, (cost + grid[nr][nc], nr, nc, nxt_fuel))
    return -1
```

**例题：** LC 1091 二进制矩阵中的最短路径

给 `n x n` 的 0/1 矩阵 `grid`，求从左上角 `(0, 0)` 到右下角 `(n-1, n-1)` 的最短**畅通路径**的长度，不存在返回 `-1`。畅通路径要求经过的格子值都是 `0`，相邻格子在 **8 个方向**之一上连通（共边或共角）；路径长度是**经过的格子总数**。`n == grid.length == grid[i].length`，`1 <= n <= 100`，`grid[i][j]` 为 `0` 或 `1`。

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

**例题：** 量水问题：最短操作序列

两个容量分别为 `x`、`y` 升的水壶，水源无限。允许三种操作：把任一水壶灌满；把任一水壶倒空；把一个水壶的水倒进另一个，直到倒的壶空了或者另一个壶满了。要得到恰好 `z` 升水（先和面试官确认 `z` 的含义：默认是两个壶里的水量之和，也可以是「某一个壶里」），**输出操作次数最少的操作序列**，做不到返回 `None`，`z = 0` 返回空列表。`1 <= x, y <= 10^3`，`0 <= z <= 2 * 10^3`。

```python
from collections import deque
from math import gcd
def jug_steps(x: int, y: int, z: int, single: bool = False) -> list[str] | None:
    """两个水壶容量 x、y。得到恰好 z 升（single=False：两壶之和；True：某一壶里）的最短操作序列；做不到返回 None。"""
    top = max(x, y) if single else x + y
    if z < 0 or z > top or z % gcd(x, y):
        return None
    def hit(a: int, b: int) -> bool:
        return z in (a, b) if single else a + b == z
    start = (0, 0)
    parent: dict[tuple[int, int], tuple[tuple[int, int], str] | None] = {start: None}
    queue = deque([start])
    while queue:
        a, b = state = queue.popleft()
        if hit(a, b):
            ops: list[str] = []
            while parent[state] is not None:
                state, op = parent[state]
                ops.append(op)
            return ops[::-1]
        pour_ab, pour_ba = min(a, y - b), min(b, x - a)
        moves = (((x, b), "fill X"), ((a, y), "fill Y"), ((0, b), "empty X"), ((a, 0), "empty Y"),
                 ((a - pour_ab, b + pour_ab), "pour X->Y"), ((a + pour_ba, b - pour_ba), "pour Y->X"))
        for nxt, op in moves:
            if nxt not in parent:
                parent[nxt] = ((a, b), op)
                queue.append(nxt)
    return None
```
