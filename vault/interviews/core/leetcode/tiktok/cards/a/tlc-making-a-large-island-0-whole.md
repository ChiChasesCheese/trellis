---
id: tlc-making-a-large-island-0-whole
node: a.making-a-large-island
type: qa
---
## Q
**LC 827 最大人工岛**｜Hard · TikTok 高频

给 `n x n` 的二进制矩阵 `grid`，**最多**只能将一格 `0` 变成 `1`。返回执行此操作后，`grid` 中最大的岛屿面积。岛屿由一组上、下、左、右四个方向相连的 `1` 形成。`n == grid.length == grid[i].length`，`1 <= n <= 500`，`grid[i][j]` 为 `0` 或 `1`。例：`[[1,0],[0,1]]` → `3`（翻一格 `0` 连通两个小岛）；`[[1,1],[1,0]]` → `4`；`[[1,1],[1,1]]` → `4`（没有 `0` 可翻，面积不变）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先给每座岛编号并统计面积（一次遍历）；再枚举每个 `0`，把它上下左右**不同**岛屿的面积加起来再加 `1`，取最大；若没有 `0`，答案是原有最大岛。`O(n^2)`。

**识别。** 「改变一个格子使连通块最大」：暴力是每个 `0` 翻一次重算，但翻转只会把它四周的岛屿连在一起，其他岛屿不受影响，所以可以**预处理每座岛的面积**，翻转时只做加法。`n` 到 `500`，格子 `2.5×10^5` 个，暴力 `O(n^4)` 不行，要 `O(n^2)`。是连通分量（connected components）加枚举的组合；DFS 的递归深度可达 `2.5×10^5`，必须用显式栈。

**推导。** 暴力：对每个 `0`，翻成 `1`，整个矩阵重新求最大岛，`O(n^2)` 个 `0` × `O(n^2)` = `O(n^4)` → 浪费：每次都重算所有岛 → 预处理：用 DFS/BFS 给每座岛一个编号，记 `size[编号]` → 对每个 `0`，看上下左右邻居的编号，**去重**后把对应面积相加再加 `1`（翻转格自己），每个 `0` 只花常数时间。

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

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                label[i][j] = tag
                stack, area = [(i, j)], 0          # 显式栈：n = 500 时递归会爆
                while stack:
                    x, y = stack.pop()
                    area += 1
                    for a, b in neighbors(x, y):
                        if grid[a][b] == 1 and label[a][b] == 0:
                            label[a][b] = tag
                            stack.append((a, b))
                size[tag] = area
    best = max(size.values(), default=0)           # 一格都不翻（或没有 0 可翻）
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}   # 集合去重：同一座岛可能从几个方向碰到
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))   # 水的编号是 0，不在 size 里，记 0
    return best
```

运行：`[[1,0],[0,1]]` → `3`，`[[1,1],[1,0]]` → `4`，`[[1,1],[1,1]]` → `4`，`[[0]]` → `1`，`[[1]]` → `1`，`[[0,0],[0,0]]` → `1`；`500×500` 全 `1` 只在中间留一个 `0` → `250000`。

**复杂度。** 时间 `O(n^2)`：标号一遍，枚举 `0` 一遍，每格常数；空间 `O(n^2)`：`label` 与栈。

**易错点。**
- 邻居岛屿必须去重：`[[1,1],[1,0]]` 中 `0` 的上方和左方是同一座面积 `3` 的岛，不去重加成 `3 + 3 + 1 = 7`，正确是 `3 + 1 = 4`。
- 没有 `0` 可翻时答案是原有最大岛：`best` 要先用 `max(size.values(), default=0)` 初始化，否则全 `1` 的 `[[1,1],[1,1]]` 会返回 `0`，正确是 `4`。
- 全是 `0` 时 `size` 为空：`default=0` 防止 `max` 抛 `ValueError`，翻一格得到 `1`。

**追问。**
- 并查集（Union-Find）版：不遍历 DFS，扫描时合并相邻的 `1`，岛面积存在根节点上。
- 最多翻 `k` 格：不再是邻居相加，要在「翻转预算」下做搜索（LC 1568 一类），复杂度上升。
- 求翻哪一格：记录取最大时的 `(i, j)`。

**同模式。** LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 934 最短的桥、LC 1020 飞地的数量。
