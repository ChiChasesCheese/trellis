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

**带状态的 BFS**
- LC 1293 网格中的最短路径（状态含剩余消除次数）

**无权最短路（BFS）**
- LC 127 单词接龙
- LC 815 公交路线
- LC 994 腐烂的橘子（多源）
- LC 286 墙与门（多源）
- LC 934 最短的桥（多源）
- LC 317 离建筑物最近的距离（对每栋楼各做一次 BFS）

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

**例题：** LC 934 最短的桥

`n x n` 的 0/1 矩阵（`2 <= n <= 100`）里恰好有两座岛（上下左右相连的 `1`），求把两座岛连在一起最少需要翻转的 `0` 的个数。

```python
from collections.abc import Iterator
def shortest_bridge(grid: list[list[int]]) -> int:
    n = len(grid)
    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b
    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j])
    seen = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for a, b in neighbors(x, y):
            if grid[a][b] and (a, b) not in seen:
                seen.add((a, b))
                stack.append((a, b))
    frontier = list(seen)
    flips = 0
    while frontier:
        nxt: list[tuple[int, int]] = []
        for x, y in frontier:
            for a, b in neighbors(x, y):
                if (a, b) not in seen:
                    if grid[a][b]:
                        return flips
                    seen.add((a, b))
                    nxt.append((a, b))
        frontier = nxt
        flips += 1
    return -1
```

**例题：** LC 317 离建筑物最近的距离

网格（`m, n <= 50`）中 `0` 空地、`1` 建筑、`2` 障碍，建筑和障碍不能通过；在一块空地上盖房子，使它到所有建筑的步行距离之和最小，返回这个和，不存在返回 `-1`。

```python
from collections import deque
def shortest_distance(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    total = [[0] * n for _ in range(m)]
    reach = [[0] * n for _ in range(m)]
    buildings = 0
    for br in range(m):
        for bc in range(n):
            if grid[br][bc] != 1:
                continue
            buildings += 1
            seen = [[False] * n for _ in range(m)]
            seen[br][bc] = True
            queue = deque([(br, bc)])
            dist = 0
            while queue:
                dist += 1
                for _ in range(len(queue)):
                    r, c = queue.popleft()
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and not seen[nr][nc]:
                            seen[nr][nc] = True
                            total[nr][nc] += dist
                            reach[nr][nc] += 1
                            queue.append((nr, nc))
    return min((total[r][c] for r in range(m) for c in range(n)
                if grid[r][c] == 0 and reach[r][c] == buildings), default=-1)
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
