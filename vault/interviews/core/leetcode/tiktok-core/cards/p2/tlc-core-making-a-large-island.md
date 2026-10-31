---
id: tlc-core-making-a-large-island
node: p2.making-a-large-island
type: qa
---
## Q
**LC 827 最大人工岛**｜Hard · LC TikTok 近 30 天热度 82/100（全时段 75） · CodeTop 国内累计 1 次 · 最近 2026-09-02（国内 CodeTop） · 也在：Amazon

给 `n x n` 的二进制矩阵 `grid`，**最多**只能将一格 `0` 变成 `1`。返回执行此操作后，`grid` 中最大的岛屿面积。岛屿由一组上、下、左、右四个方向相连的 `1` 形成。`n == grid.length == grid[i].length`，`1 <= n <= 500`，`grid[i][j]` 为 `0` 或 `1`。例：`[[1,0],[0,1]]` → `3`（翻一格 `0` 连通两个小岛）；`[[1,1],[1,0]]` → `4`；`[[1,1],[1,1]]` → `4`（没有 `0` 可翻，面积不变）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先给每座岛编号并统计面积（一次遍历）；再枚举每个 `0`，把它上下左右**不同**岛屿的面积加起来再加 `1`，取最大；若没有 `0`，答案是原有最大岛。`O(n^2)`。

**识别。** 「改变一个格子使连通块最大」：暴力是每个 `0` 翻一次重算，但翻转只会把它四周的岛屿连在一起，其他岛屿不受影响，所以可以**预处理每座岛的面积**，翻转时只做加法。`n` 到 `500`，格子 `2.5×10^5` 个，暴力 `O(n^4)` 不行，要 `O(n^2)`。是连通分量（connected components）加枚举的组合；连通分量用递归 DFS 最直观（每座岛一次 `dfs`，返回面积）。

**推导。** 暴力：对每个 `0`，翻成 `1`，整个矩阵重新求最大岛，`O(n^2)` 个 `0` × `O(n^2)` = `O(n^4)` → 浪费：每次都重算所有岛 → 预处理：用 DFS/BFS 给每座岛一个编号，记 `size[编号]` → 对每个 `0`，看上下左右邻居的编号，**去重**后把对应面积相加再加 `1`（翻转格自己），每个 `0` 只花常数时间。

**简单解法。** 暴力：每个 `0` 真的翻成 `1`，BFS 数出它所在岛的面积，再翻回去，取最大。

```python
from collections import deque


def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)

    def area_from(i: int, j: int) -> int:           # 从 (i, j) 出发数连通的 1
        seen = {(i, j)}
        queue = deque([(i, j)])
        while queue:
            x, y = queue.popleft()
            for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in seen:
                    seen.add((a, b))
                    queue.append((a, b))
        return len(seen)

    best = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                grid[i][j] = 1                      # 真的翻一格，只数被翻那格所在的岛：
                best = max(best, area_from(i, j))   # 不占满全图的岛都挨着某个 0，翻开它面积只增不减
                grid[i][j] = 0                      # 翻回去
    return best if best else n * n                  # 没有 0 可翻：整张图就是一座岛
```

时间 `O(n^4)`，空间 `O(n^2)`；`n = 500` 跑不完，作开场答案能说明正确性，再指出「翻转只影响四周的岛」引到先给岛编号、记面积。

最优解：

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

运行：`[[1,0],[0,1]]` → `3`，`[[1,1],[1,0]]` → `4`，`[[1,1],[1,1]]` → `4`，`[[0]]` → `1`，`[[1]]` → `1`，`[[0,0],[0,0]]` → `1`；`500×500` 全 `1` 只在中间留一个 `0` → `250000`（调大递归上限后）；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n^2)`：标号一遍，枚举 `0` 一遍，每格常数；空间 `O(n^2)`：`label` 与递归栈。

**拓展优化。**
- 递归深度：蛇形岛让 `dfs` 嵌套到约 `2.5 * 10^5` 层，超过默认约 1000 会抛 `RecursionError`。把 `dfs` 换成显式栈 `flood`，其余不变（`size[tag] = flood(grid, label, i, j, tag)`）：
```python
def flood(grid: list[list[int]], label: list[list[int]], i: int, j: int, tag: int) -> int:
    """给 (i, j) 所在的岛打上 tag，返回面积；用来替换递归的 dfs。"""
    n = len(grid)
    label[i][j] = tag
    stack, area = [(i, j)], 0
    while stack:
        x, y = stack.pop()
        area += 1
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and label[a][b] == 0:
                label[a][b] = tag                   # 入栈时就打标，同一格不会入栈两次
                stack.append((a, b))
    return area
```
- 并查集（Union-Find）：不搜索，合并相邻的 `1`，面积存在根上；枚举 `0` 时对邻居取根并去重求和，其余同主解：
```python
def largest_island_uf(grid: list[list[int]]) -> int:
    n = len(grid)
    parent = list(range(n * n))
    size = [1] * (n * n)                            # 只有根节点的 size 有意义

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]           # 路径折半
            x = parent[x]
        return x

    for i in range(n):
        for j in range(n):
            if grid[i][j] != 1:
                continue
            for a, b in ((i + 1, j), (i, j + 1)):   # 只向右、向下合并，每对邻居处理一次
                if a < n and b < n and grid[a][b] == 1:
                    ra, rb = find(i * n + j), find(a * n + b)
                    if ra != rb:
                        if size[ra] < size[rb]:
                            ra, rb = rb, ra         # 小的并到大的下面
                        parent[rb] = ra
                        size[ra] += size[rb]
    best = max((size[find(i * n + j)] for i in range(n) for j in range(n) if grid[i][j] == 1), default=0)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                roots = {find(a * n + b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                         if 0 <= a < n and 0 <= b < n and grid[a][b] == 1}   # 集合去重：同一座岛只算一次
                best = max(best, 1 + sum(size[r] for r in roots))
    return best
```

**易错点。**
- 邻居岛屿必须去重：`[[1,1],[1,0]]` 中 `0` 的上方和左方是同一座面积 `3` 的岛，不去重加成 `3 + 3 + 1 = 7`，正确是 `3 + 1 = 4`。
- 没有 `0` 可翻时答案是原有最大岛：`best` 要先用 `max(size.values(), default=0)` 初始化，否则全 `1` 的 `[[1,1],[1,1]]` 会返回 `0`，正确是 `4`。
- 全是 `0` 时 `size` 为空：`default=0` 防止 `max` 抛 `ValueError`，翻一格得到 `1`。
- 递归深度：一座岛是 `500×500` 的蛇形或全 `1` 时，`dfs` 深度可达 `2.5×10^5`，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成显式栈（见拓展优化）。

**追问。**
- 最多翻 `k` 格：不再是邻居相加，要在「翻转预算」下做搜索（LC 1568 一类），复杂度上升。
- 求翻哪一格：记录取最大时的 `(i, j)`。

**同模式。** LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 934 最短的桥、LC 1020 飞地的数量。
