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
- 岛屿数量及其追问集合（高频）

**多源 BFS / 分层**
- LC 994 腐烂的橘子
- LC 286 墙与门

**隐式图的最短步数**
- LC 127 单词接龙
- LC 815 公交路线
- LC 1293 网格中的最短路径（状态里带"剩余可消除障碍数"）
- LC 1091 二进制矩阵中的最短路径（高频）
- 量水问题：最短操作序列（高频）

**图的建模与染色**
- LC 133 克隆图（哈希：旧节点 → 新节点）
- LC 886 可能的二分法（染色）
- LC 399 除法求值（带权图）
- LC 2385 感染二叉树需要的总时间（高频）
- LC 863 二叉树中所有距离为 K 的结点（高频）

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

**例题：** 岛屿数量及其追问集合

给一个 `m x n` 的二维 0/1 网格 `grid`，`1 <= m, n <= 300`，`1` 是陆地、`0` 是水，上下左右相连的陆地构成一座岛屿。依次回答：（1）岛屿数量，**不能修改**原网格；（2）形状不同的岛屿数量（只允许平移）；（3）旋转、翻转后相同也算同一种形状。

```python
from collections.abc import Iterator
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
def components(grid: list[list[int]]) -> Iterator[list[tuple[int, int]]]:
    """逐个产出岛屿的格子列表；不修改 grid，visited 单独记。"""
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    def dfs(x: int, y: int, cells: list[tuple[int, int]]) -> None:
        seen[x][y] = True
        cells.append((x, y))
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and not seen[nx][ny]:
                dfs(nx, ny, cells)
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and not seen[r][c]:
                cells: list[tuple[int, int]] = []
                dfs(r, c, cells)
                yield cells
def num_islands(grid: list[list[int]]) -> int:
    return sum(1 for _ in components(grid))
def num_distinct_islands(grid: list[list[int]]) -> int:
    """形状相同（只允许平移）算同一种：格子坐标减去最小的 (行, 列) 后排序，作为形状签名。"""
    shapes = set()
    for cells in components(grid):
        r0, c0 = min(cells)
        shapes.add(tuple(sorted((r - r0, c - c0) for r, c in cells)))
    return len(shapes)
TRANSFORMS = (lambda x, y: (x, y), lambda x, y: (x, -y), lambda x, y: (-x, y), lambda x, y: (-x, -y),
              lambda x, y: (y, x), lambda x, y: (y, -x), lambda x, y: (-y, x), lambda x, y: (-y, -x))
def num_distinct_islands_ii(grid: list[list[int]]) -> int:
    """旋转、翻转后相同也算同一种：8 种变换各自归一化，取字典序最小的作为签名。"""
    shapes = set()
    for cells in components(grid):
        forms = []
        for f in TRANSFORMS:
            pts = [f(x, y) for x, y in cells]
            x0, y0 = min(pts)
            forms.append(tuple(sorted((x - x0, y - y0) for x, y in pts)))
        shapes.add(min(forms))
    return len(shapes)
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

**例题：** LC 2385 感染二叉树需要的总时间

给二叉树的根节点 `root`，树中节点的值**互不相同**，再给整数 `start`。第 `0` 分钟，值为 `start` 的节点开始被感染。之后每分钟，满足下面两个条件的节点会被感染：此前没有被感染；与一个已被感染的节点**相邻**（父子相邻）。返回感染整棵树需要的分钟数。节点数在 `[1, 10^5]`，`1 <= Node.val <= 10^5`，值互不相同，树中一定存在值为 `start` 的节点。

```python
from collections import defaultdict, deque
def amount_of_time(root: TreeNode, start: int) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    def link(node: TreeNode) -> None:
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                link(child)
    link(root)
    queue = deque([start])
    seen = {start}
    minutes = -1
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            u = queue.popleft()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
    return minutes
```

**例题：** LC 863 二叉树中所有距离为 K 的结点

给二叉树的根结点 `root`、树中的一个目标结点 `target` 和整数 `k`，返回到 `target` 距离恰为 `k` 的所有结点的值（距离是两结点间路径的边数，可以向上也可以向下走），顺序任意。结点数在 `[1, 500]`，`0 <= Node.val <= 500` 且互不相同，`0 <= k <= 1000`。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    frontier, seen = [target], {target}
    for _ in range(k):
        nxt: list[TreeNode] = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
    return [node.val for node in frontier]
```
