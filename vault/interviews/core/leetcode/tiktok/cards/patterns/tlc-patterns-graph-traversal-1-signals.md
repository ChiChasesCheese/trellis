---
id: tlc-patterns-graph-traversal-1-signals
node: patterns.graph-traversal
type: qa
step: 1
---
## Q
**图与网格的 BFS / DFS（Graph Traversal）｜信号**

什么样的题面该想到图遍历？DFS 与 BFS 怎么选？多源 BFS、隐式图各由什么信号触发？

## A
**触发信号：**
- 输入是**网格**（`0/1`、`'1'/'0'`、高度矩阵）并且问「连通块 / 岛屿 / 面积 / 能否到达」→ DFS 或 BFS 染色（例：LC 200 岛屿数量）。
- 输入是**边列表 / 邻接关系**（先修课、对立关系、道路）→ 先建邻接表，再遍历（例：LC 1466 重新规划路线；高频：LC 886 可能的二分法）。
- 问**最少步数 / 最短转换次数**，每步代价相同 → **BFS**，第一次到达就是最短（例：LC 1091 二进制矩阵中的最短路径）。
- 题面没有"图"字，但**状态之间有转移**：单词改一个字母 → **隐式图**，BFS 里动态生成邻居（例：LC 127 单词接龙）。
- 「**多个起点同时扩散**」：所有起点一起入队 → **多源 BFS**（例：LC 286 墙与门）。
- 「从边界反向找」：从海洋出发反向遍历，比从每个格子出发高效（例：LC 417 太平洋大西洋水流问题）。

**DFS 还是 BFS：**
- 连通块计数、面积、能不能到达 → 都可以，DFS 写起来短；但递归深度可达 `m * n`，Python 默认限制约 1000，网格大时要改显式栈或 BFS（例：LC 695 岛屿的最大面积；高频：LC 827 最大人工岛）。
- **最短路 / 最少步数 / 按层扩散** → 只能 BFS，按层数就是时间（例：LC 994 腐烂的橘子；高频：LC 2385 感染二叉树需要的总时间）。
- 需要记录路径或回溯 → DFS，进入时加入路径，退出时弹出（例：LC 113 路径总和 II；高频：LC 79 单词搜索）。

**近似信号：**
- 边有权重且不相等 → Dijkstra（最短路一组）（例：LC 778 水位上升的泳池中游泳）。
- 有向图判环、依赖顺序 → 拓扑排序（例：LC 207 课程表）。
- 动态连边、问是否连通 → 并查集（例：LC 323 无向图中连通分量的数目）。
- 只要连通块个数且数据可以离线 → 并查集与 DFS 都行（例：LC 547 省份数量）。

**例题：** LC 200 岛屿数量

`'1'` 是陆地、`'0'` 是水，`m x n` 网格，上下左右相连的陆地算一个岛，求岛屿数，`1 <= m, n <= 300`。

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

**例题：** LC 1466 重新规划路线

`n` 座城市由 `n - 1` 条有向路线连成一棵树，求最少改变几条路线方向，才能让所有城市都能到达城市 0，`2 <= n <= 5 * 10^4`。

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

**例题：** LC 1091 二进制矩阵中的最短路径

`n x n` 的 0/1 矩阵，只走值为 0 的格子、可朝 8 个方向走，求左上角到右下角的最短路径长度（格子数），不存在返回 `-1`，`1 <= n <= 100`。

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

**例题：** LC 127 单词接龙

每次只改一个字母且结果必须在 `wordList` 里，求从 `beginWord` 到 `endWord` 的最短转换序列的单词数，不存在返回 `0`，`wordList.length <= 5000`，单词长度 `<= 10`。

```python
from collections import deque
import string
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

**例题：** LC 286 墙与门

`m x n` 网格里 `-1` 是墙、`0` 是门、`2147483647` 是空房间，给每个空房间填上到最近门的距离，到不了则保持原值，`1 <= m, n <= 250`。

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

**例题：** LC 417 太平洋大西洋水流问题

高度矩阵，水可以流向高度小于等于当前格的相邻格；返回既能流到太平洋（上、左边界）又能流到大西洋（下、右边界）的所有格子，`1 <= m, n <= 200`。

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

**例题：** LC 695 岛屿的最大面积

`m x n` 的 0/1 网格，上下左右相连的 1 组成岛屿，求最大岛屿的面积，没有岛屿返回 `0`，`1 <= m, n <= 50`。

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

**例题：** LC 994 腐烂的橘子

网格里 `0` 空、`1` 新鲜、`2` 腐烂，每分钟腐烂橘子使上下左右的新鲜橘子腐烂，求全部腐烂所需的最少分钟数，不可能返回 `-1`，`1 <= m, n <= 10`。

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

**例题：** LC 113 路径总和 II

在二叉树里找出所有从根到叶子、节点值之和等于 `targetSum` 的路径，节点数 `[0, 5000]`。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(node: TreeNode | None, rest: int) -> None:
        if node is None:
            return
        path.append(node.val)
        rest -= node.val
        if node.left is None and node.right is None and rest == 0:
            res.append(path[:])
        dfs(node.left, rest)
        dfs(node.right, rest)
        path.pop()
    dfs(root, target_sum)
    return res
```

**例题：** LC 778 水位上升的泳池中游泳

`n x n` 网格 `grid[i][j]` 是平台高度，时间 `t` 时水位为 `t`，只能在两个相邻平台都被淹没时移动；求从左上角游到右下角的最少时间，`1 <= n <= 50`，高度互不相同。

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

**例题：** LC 207 课程表

`numCourses` 门课、先修关系 `prerequisites`，判断能否修完所有课，`1 <= numCourses <= 2000`。

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

**例题：** LC 323 无向图中连通分量的数目

`n` 个节点、无向边列表 `edges`，求连通分量的个数，`1 <= n <= 2000`，`edges.length <= 5000`。

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    return comps
```

**例题：** LC 547 省份数量

给 `n x n` 邻接矩阵 `isConnected`（对称，对角线全为 1），直接或间接相连的城市算一个省份，求省份总数，`1 <= n <= 200`。

```python
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
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

**例题：** LC 886 可能的二分法

把编号 `1..n` 的人分成两组，`dislikes[i] = [a, b]` 表示 `a` 和 `b` 不能在同一组，判断能否分成功；`1 <= n <= 2000`，`0 <= dislikes.length <= 10^4`。

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

**例题：** LC 827 最大人工岛

`n x n` 的 0/1 矩阵 `grid`，最多把一格 `0` 变成 `1`，返回操作后最大的岛屿面积（岛由四方向相连的 `1` 组成）；`1 <= n <= 500`。

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

**例题：** LC 2385 感染二叉树需要的总时间

二叉树各节点的值互不相同，值为 `start` 的节点在第 `0` 分钟被感染，之后每分钟感染与已感染节点相邻（父子）的节点；返回感染整棵树需要的分钟数；节点数 `<= 10^5`。

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

**例题：** LC 79 单词搜索

在字符网格 `board` 里判断单词 `word` 是否存在：沿水平或竖直相邻的格子依次拼出，同一格在一条路径里不能重复使用；`1 <= m, n <= 6`，`1 <= word.length <= 15`。

```python
from collections import Counter
from itertools import chain
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    board_count = Counter(chain.from_iterable(board))
    if Counter(word) - board_count:
        return False
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]
    def dfs(r: int, c: int, k: int) -> bool:
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        board[r][c] = "#"
        found = any(
            0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1)
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
        board[r][c] = word[k]
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```
