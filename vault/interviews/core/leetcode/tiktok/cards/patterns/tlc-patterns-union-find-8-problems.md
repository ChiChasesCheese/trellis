---
id: tlc-patterns-union-find-8-problems
node: patterns.union-find
type: qa
step: 8
---
## Q
**并查集（Union-Find）｜本组用到并查集的题**

按变形分类，这个题组里哪些题可以用并查集？

## A
**连通块与分组**
- LC 200 岛屿数量（并查集是 DFS 的替代写法）
- LC 695 岛屿的最大面积（按块大小取最大）
- LC 827 最大人工岛（合并后读取相邻块的大小）
- LC 721 账户合并
- LC 128 最长连续序列（`x` 与 `x + 1` 合并，取最大块）
- LC 924 尽量减少恶意软件的传播
- LC 323 无向图中连通分量的数目（高频）

**判环与最小生成树**
- LC 1584 连接所有点的最小费用（Kruskal）

**等价关系**
- LC 886 可能的二分法（拆点：A 组 / B 组）
- LC 399 除法求值（带权并查集）

提示：看到"逐步合并 / 是否同组 / 加边是否成环"就想并查集；再确认是否需要权重、是否要统计块大小、节点是否需要先映射成编号。

**例题：** LC 200 岛屿数量

由 `'1'`（陆地）和 `'0'`（水）组成的网格，数四连通陆地块（岛屿）的个数。`1 <= m, n <= 300`。

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

**例题：** LC 695 岛屿的最大面积

0/1 网格，四连通的 `1` 组成岛屿，返回最大的岛屿面积（没有则为 `0`）。`1 <= m, n <= 50`。

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

**例题：** LC 827 最大人工岛

`n x n` 的 0/1 网格，最多把一个 `0` 变成 `1`，返回此后最大的岛屿面积（四连通）。`1 <= n <= 500`。

```python
from collections.abc import Iterator
def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    label = [[0] * n for _ in range(n)]            # 0 = 水或还没编号；岛从 1 开始编号
    size: dict[int, int] = {}                      # 岛编号 -> 面积
    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b
    def dfs(i: int, j: int, tag: int) -> int:      # 给这座岛的每一格打上 tag，返回面积
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
    best = max(size.values(), default=0)           # 一格都不翻（或没有 0 可翻）
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}   # 集合去重：同一座岛可能从几个方向碰到
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))   # 水的编号是 0，不在 size 里，记 0
    return best
```

**例题：** LC 721 账户合并

`accounts[i]` 是 `[名称, 邮箱...]`，两个账户有共同邮箱就属于同一个人（同名不一定同人）。合并后每个账户为 `[名称, 排序后的邮箱...]`，账户顺序任意。`1 <= accounts.length <= 1000`，每个账户 `2..10` 个元素。

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

**例题：** LC 128 最长连续序列

未排序整数数组 `nums`，求数值连续的最长序列的长度，要求 `O(n)`。`0 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`。

```python
def longest_consecutive(nums: list[int]) -> int:
    seen = set(nums)                   # 去重 + O(1) 查询
    best = 0
    for x in seen:
        if x - 1 in seen:              # x 不是序列的起点：跳过，让起点去数
            continue
        end = x + 1
        while end in seen:             # 从起点向右数下去
            end += 1
        best = max(best, end - x)
    return best
```

**例题：** LC 924 尽量减少恶意软件的传播

`n x n` 邻接矩阵 `graph` 和初始被感染的节点 `initial`，相连的节点只要一个被感染就会全部感染。从 `initial` 中恰好移除一个节点，使最终感染总数最小，返回该节点（并列取下标最小）。`2 <= n <= 300`。

```python
from collections import Counter
def min_malware_spread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径折半
            x = parent[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                parent[find(i)] = find(j)      # 合并连通块
    size = Counter(find(i) for i in range(n))                 # 每个连通块的大小
    infected = Counter(find(x) for x in initial)              # 每个连通块里的初始感染数
    best, best_saved = min(initial), 0                        # 救不了任何节点时，返回下标最小的
    for x in sorted(initial):                                 # 升序遍历，严格大于才替换 -> 并列取最小下标
        root = find(x)
        if infected[root] == 1 and size[root] > best_saved:   # 块里只有它一个感染源：移除它能救整个块
            best, best_saved = x, size[root]
    return best
```

**例题：** LC 1584 连接所有点的最小费用

平面上的点 `points`，连接两点的费用是曼哈顿距离，求把所有点连成一棵树的最小总费用。`1 <= points.length <= 1000`，`|xi|, |yi| <= 10^6`，点互不相同。

```python
def min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    INF = 1 << 60
    dist = [INF] * n                       # dist[i]：i 到已选集合的最短曼哈顿距离
    dist[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=dist.__getitem__)   # 离集合最近的未选点
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

**例题：** LC 886 可能的二分法

把 `1..n` 的人分成两组，`dislikes[i] = [a, b]` 表示 `a`、`b` 不能同组，判断能否分成。`1 <= n <= 2000`，`0 <= dislikes.length <= 10^4`。

```python
from collections import deque
def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    color = [0] * (n + 1)                          # 0 = 未分组，1 / -1 = 两个组
    for start in range(1, n + 1):                  # 图可能不连通：每个连通块都要查
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:           # 互相讨厌的人落在同一组
                    return False
                if color[v] == 0:
                    color[v] = -color[u]           # 敌人的敌人放另一组
                    queue.append(v)
    return True
```

**例题：** LC 399 除法求值

已知若干 `Ai / Bi = values[i]`，对每个查询 `[C, D]` 返回 `C / D`，算不出来（含未出现的变量）返回 `-1.0`。`equations.length, queries.length <= 20`，`0.0 < values[i] <= 20.0`。

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

`n` 个节点（`0..n-1`）和无向边列表 `edges`，返回连通分量的个数；`1 <= n <= 2000`，`1 <= edges.length <= 5000`。

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
