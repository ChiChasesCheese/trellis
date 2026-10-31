---
id: tlc-patterns-graph-traversal-8-problems
node: patterns.graph-traversal
type: qa
step: 8
---
## Q
**图与网格的 BFS / DFS｜本组用到图遍历的题**

按变形分类，这个题组里哪些题属于图与网格遍历？

## A
**连通块（DFS / BFS）**
- LC 200 岛屿数量
- LC 695 岛屿的最大面积
- LC 694 不同岛屿的数量
- LC 827 最大人工岛
- LC 417 太平洋大西洋水流问题（从边界反向遍历）

**多源 BFS / 分层**
- LC 994 腐烂的橘子
- LC 286 墙与门
- LC 934 最短的桥
- LC 317 离建筑物最近的距离（从每栋楼各做一次 BFS）

**隐式图的最短步数**
- LC 127 单词接龙
- LC 815 公交路线
- LC 1293 网格中的最短路径（状态里带"剩余可消除障碍数"）

**图的建模与染色**
- LC 133 克隆图（哈希：旧节点 → 新节点）
- LC 886 可能的二分法（染色）
- LC 1466 重新规划路线（树形无向图 + 方向标记）
- LC 399 除法求值（带权图）
- LC 924 尽量减少恶意软件的传播（连通块）

提示：先判定是求连通性（DFS）还是求最少步数（BFS）；再决定节点是什么、邻居怎么生成；`seen` 一律在入队时标记。

**例题：** LC 200 岛屿数量

给由 `'1'`（陆地）和 `'0'`（水）组成的 `m x n` 网格（`m, n <= 300`），数上下左右相连的陆地块（岛屿）的个数。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

**例题：** LC 695 岛屿的最大面积

给 `m x n` 的 0/1 网格（`m, n <= 50`），岛屿是上下左右相连的 `1`，求面积（`1` 的个数）最大的岛屿，没有岛屿返回 `0`。

```python
from itertools import product
def max_area_of_island(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    def dfs(i: int, j: int) -> int:
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
            return 0
        grid[i][j] = 0
        return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)
    return max(dfs(i, j) for i, j in product(range(m), range(n)))
```

**例题：** LC 694 不同岛屿的数量

给 0/1 网格（`m, n <= 50`），统计形状不同的岛屿数；两个岛屿相同当且仅当其中一个只靠平移就能与另一个重合（不能旋转、翻转）。

```python
def num_distinct_islands(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    shapes: set[frozenset[tuple[int, int]]] = set()
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != 1 or seen[r0][c0]:
                continue
            seen[r0][c0] = True
            stack = [(r0, c0)]
            cells: list[tuple[int, int]] = []
            while stack:
                r, c = stack.pop()
                cells.append((r - r0, c - c0))
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            shapes.add(frozenset(cells))
    return len(shapes)
```

**例题：** LC 827 最大人工岛

给 `n x n` 的 0/1 网格（`n <= 500`），最多把一个 `0` 变成 `1`，求之后最大的岛屿面积。

```python
from collections.abc import Iterator
def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    label = [[0] * n for _ in range(n)]
    size: dict[int, int] = {}
    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b
    def dfs(i: int, j: int, tag: int) -> int:
        label[i][j] = tag
        area = 1
        for a, b in neighbors(i, j):
            if grid[a][b] == 1 and label[a][b] == 0:
                area += dfs(a, b, tag)
        return area
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                size[tag] = dfs(i, j, tag)
    best = max(size.values(), default=0)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))
    return best
```

**例题：** LC 417 太平洋大西洋水流问题

给高度矩阵 `heights`（`m, n <= 200`），太平洋在左、上边界，大西洋在右、下边界，水可以流向上下左右高度不高于当前格的邻格；返回所有既能流到太平洋、又能流到大西洋的格子坐标。

```python
def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    m, n = len(heights), len(heights[0])
    def reach(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
        seen: set[tuple[int, int]] = set()
        def dfs(r: int, c: int) -> None:
            seen.add((r, c))
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    dfs(nr, nc)
        for r, c in starts:
            if (r, c) not in seen:
                dfs(r, c)
        return seen
    pacific = reach([(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)])
    atlantic = reach([(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)])
    return sorted([r, c] for r, c in pacific & atlantic)
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

**例题：** LC 133 克隆图

给无向连通图中一个节点的引用（节点数 `<= 100`，`val` 互不相同），返回该图的深拷贝。

```python
def clone_graph(node: Node | None) -> Node | None:
    copies: dict[Node, Node] = {}
    def dfs(cur: Node) -> Node:
        if cur in copies:
            return copies[cur]
        copies[cur] = clone = Node(cur.val)
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone
    return dfs(node) if node else None
```

**例题：** LC 886 可能的二分法

把编号 `1..n` 的人（`n <= 2000`）分成两组，`dislikes`（`<= 10^4` 对）里的两个人不能在同一组，判断能否做到。

```python
from collections import deque
def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    color = [0] * (n + 1)
    for start in range(1, n + 1):
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:
                    return False
                if color[v] == 0:
                    color[v] = -color[u]
                    queue.append(v)
    return True
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

**例题：** LC 924 尽量减少恶意软件的传播

`n` 个节点（`n <= 300`）的无向图用邻接矩阵给出，`initial` 是初始被感染的节点，感染沿边传播到整个连通块；移除 `initial` 中恰好一个节点，使最终感染节点总数最小，有多个答案返回下标最小的。

```python
from collections import Counter
def min_malware_spread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                parent[find(i)] = find(j)
    size = Counter(find(i) for i in range(n))
    infected = Counter(find(x) for x in initial)
    best, best_saved = min(initial), 0
    for x in sorted(initial):
        root = find(x)
        if infected[root] == 1 and size[root] > best_saved:
            best, best_saved = x, size[root]
    return best
```
