---
id: tlc-patterns-union-find-1-signals
node: patterns.union-find
type: qa
step: 1
---
## Q
**并查集（Union-Find）｜信号**

什么样的题面该想到并查集？它和 BFS / DFS 求连通块相比有什么取舍？

## A
并查集（Union-Find，也叫 Disjoint Set Union）维护一组**互不相交的集合**，支持两个操作：`find(x)` 找 `x` 所在集合的代表；`union(a, b)` 合并两个集合。几乎 `O(1)`（摊还 `O(α(n))`）。

**触发信号：**
- 「**是否同一组 / 是否连通**」，且关系是**逐步添加**的（动态连边）：LC 721 账户合并（共享邮箱即同一人）、LC 128 最长连续序列（例：LC 721 账户合并）。
- 「**连通块个数**」「合并之后还剩几个集合」：LC 200 的 UF 写法、LC 924（例：LC 547 省份数量）。
- 「**加入这条边会不会成环**」：最小生成树的 Kruskal 算法（LC 1584）（例：LC 1319 连通网络的操作次数）。
- 「**等价关系**」：传递性的"相等 / 同类"，如除法求值 LC 399、二分图的"敌人的敌人"LC 886（例：LC 399 除法求值）。
- 要把"相关"的元素归成组再输出（分组聚合）（例：LC 323 无向图中连通分量的数目）。

**和 DFS / BFS 的取舍：**
- 一次性给全图、只要连通块 → DFS / BFS 同样 `O(V + E)`，写起来更直接（例：LC 200 岛屿数量）。
- **边是在线逐条到来**，每加一条就要回答连通性 → 并查集（DFS 要重新跑）（例：LC 305 岛屿数量 II）。
- 要求最短路径、路径本身、层数 → 并查集做不了（只知道连通，不知道怎么走）（例：LC 1091 二进制矩阵中的最短路径）。
- 要**删除**边 → 并查集不支持，需要离线反向处理或其他结构。

**近似信号：**
- 有向图的可达性 / 先后顺序 → 拓扑排序，并查集处理的是无向关系（例：LC 1466 重新规划路线）。
- 只问相邻格子的连通 → BFS 即可（例：LC 695 岛屿的最大面积）。

**例题：** LC 721 账户合并

`accounts[i]` 的第一个元素是姓名，其余是邮箱（`1 <= accounts.length <= 1000`）；两个账户有共同邮箱就属于同一个人（同名也可能是不同人）。合并后每个账户为 `[姓名, 按字典序排好的邮箱…]`，账户顺序不限。

```python
from collections import defaultdict
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    parent = list(range(len(accounts)))        # 并查集：以账户下标为结点
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径折半
            x = parent[x]
        return x
    owner: dict[str, int] = {}                 # 邮箱 -> 第一个出现它的账户
    for i, (_, *emails) in enumerate(accounts):
        for email in emails:
            j = owner.setdefault(email, i)
            if j != i:                         # 邮箱已属于别的账户：两个账户合并
                parent[find(i)] = find(j)
    groups: defaultdict[int, list[str]] = defaultdict(list)
    for email, i in owner.items():
        groups[find(i)].append(email)
    return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]
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

**例题：** LC 399 除法求值

已知若干等式 `Ai / Bi = values[i]`（变量是长度 `1..5` 的字符串，至多 20 个等式），回答若干查询 `Cj / Dj = ?`；变量未出现或无法推出时答案为 `-1.0`。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}                 # ratio[x] = x / parent[x]
    def find(x: str) -> str:
        p = parent.setdefault(x, x)              # 第一次见到的变量自成一组
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)                       # 路径压缩：find(p) 之后 ratio[p] = p / root
            ratio[x] *= ratio[p]                 # x/root = (x/p) * (p/root)
            parent[x] = root
        return parent[x]
    for (a, b), v in zip(equations, values):     # a / b = v
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb                      # ra / rb = (a / b) * (b / rb) / (a / ra)
            ratio[ra] = v * ratio[b] / ratio[a]
    ans: list[float] = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])      # (c/root) / (d/root)
        else:
            ans.append(-1.0)                     # 变量没出现过，或不在同一个连通块
    return ans
```

**例题：** LC 323 无向图中连通分量的数目

`n` 个节点（`1 <= n <= 2000`）、`edges` 条无向边（至多 5000 条），求连通分量的个数。

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

由 `'1'`（陆地）和 `'0'`（水）组成的 `m x n` 网格（`1 <= m, n <= 300`），求岛屿数量；岛屿由水平或竖直相邻的陆地连成。

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

**例题：** LC 305 岛屿数量 II

`m x n` 的网格一开始全是水；依次给出 `positions`，每个 `[r, c]` 把该格变成陆地（可能重复），每次变化后返回当前的岛屿数（四连通）。`m * n` 很大，不能每次重扫整张图。

```python
def num_islands_ii(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent = {}                                       # 只存陆地格子，稀疏表
    size = {}
    def find(x: tuple[int, int]) -> tuple[int, int]:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    islands, answer = 0, []
    for r, c in positions:
        cell = (r, c)
        if cell in parent:                            # 重复加陆地：什么都不变
            answer.append(islands)
            continue
        parent[cell], size[cell] = cell, 1
        islands += 1                                  # 先当作新岛
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (r + dr, c + dc)
            if nb in parent:
                ra, rb = find(cell), find(nb)
                if ra != rb:                          # 每成功合并一次，岛屿数减一
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    islands -= 1
        answer.append(islands)
    return answer
```

**例题：** LC 1091 二进制矩阵中的最短路径

`n x n` 二进制矩阵（`1 <= n <= 100`），求从左上角到右下角、只经过值为 0 的格子、可沿 8 个方向移动的最短路径长度（经过的格子数），不存在返回 `-1`。

```python
from collections import deque
from itertools import product
def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1                                    # 起点或终点被堵死
    dirs = [(dr, dc) for dr, dc in product((-1, 0, 1), repeat=2) if dr or dc]   # 8 个方向
    seen = [row[:] for row in grid]                  # 1 = 障碍或已入队；不改动入参
    seen[0][0] = 1
    q = deque([(0, 0, 1)])                           # (行, 列, 路径经过的格子数)
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = 1                     # 入队时就标记，每格只入队一次
                q.append((nr, nc, d + 1))
    return -1
```

**例题：** LC 1466 重新规划路线

`n` 座城市（`2 <= n <= 5 * 10^4`）由 `n-1` 条有向路线连成一棵树，要让所有城市都能到达城市 0，求最少需要反转方向的路线数。

```python
def min_reorder(n: int, connections: list[list[int]]) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))              # 从 a 走到 b：顺着原方向，即背离城市 0，这条边要反转
        adj[b].append((a, 0))              # 从 b 走到 a：逆着原方向，即朝向城市 0，不用动
    def dfs(u: int, parent: int) -> int:   # 以 u 为根的子树里需要反转的边数
        flips = 0
        for v, cost in adj[u]:
            if v != parent:                # 树没有环：只要不走回父亲，就不会重复访问
                flips += cost + dfs(v, u)  # 进入 v 的这条边的代价 + v 子树里的代价
        return flips
    return dfs(0, -1)
```

**例题：** LC 695 岛屿的最大面积

`m x n` 二进制矩阵（`1 <= m, n <= 50`），1 表示陆地，四连通的陆地构成岛屿，求最大岛屿面积，没有岛屿返回 `0`。

```python
from itertools import product
def max_area_of_island(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    def dfs(i: int, j: int) -> int:        # 以 (i, j) 为起点沉掉整座岛，返回岛的面积
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
            return 0                       # 出界、是水、或已经沉过
        grid[i][j] = 0                     # 先沉岛再往邻居走：每格只数一次，也不会来回死循环
        return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)
    return max(dfs(i, j) for i, j in product(range(m), range(n)))
```
