# q25 · Distance to Nearest Two：练的是"两遍扫描和多源 BFS 是同一个技巧的不同维度"

> [!tldr]
> - TrueInterview 同步清单 #77（题名转述，无报告日期，本 kit 缺口补建）；**Part 2（二维网格 + 多源 BFS）为 (reconstructed)**
> - 这题考的是：数组/网格里每个 `1` 到最近 `2` 的距离，一维用两遍扫描，二维用多源 BFS，本质是同一个技巧
> - 三步套路：一维两遍扫描（左到右记最近 2，再右到左） → 意识到这是多源 BFS 在一维上的特化 → 二维直接把所有 `2` 当起点做一次 BFS
> - 最值得带走的一个模式：**"每个点到最近的一批源点的距离"永远可以用多源 BFS 解决；维度低（比如一维）时可以把 BFS 特化成更省常数的两遍扫描，但本质是同一个算法**

## 1. 题目在说什么（人话版）

数组只包含 `0`/`1`/`2`。对每个 `1`，求它到最近的 `2` 的距离；如果数组里一个 `2` 都没有，
所有 `1` 的答案是 `-1`；如果没有 `1`，输出为空。

```
arr = [2, 0, 1, 0, 1, 0, 0, 2, 1]
下标2的1：左边2在下标0，距离2
下标4的1：右边2在下标7，距离3
下标8的1：紧邻下标7的2，距离1
-> [2, 3, 1]
```

## 2. 读题：把文字变成模型

- **实体**：一维数组或二维网格，值只有 `0/1/2`；`2` 是"源点"，`1` 是要求距离的"查询点"，`0` 只是普通格子。
- **状态**：每个位置到最近源点的距离——这正是多源 BFS 要维护的 `dist` 数组。
- **一句话建模**：这是一个 **多源最短距离（多源 BFS）** 问题；一维时用两遍线性扫描特化，二维时用标准 BFS。

> [!note] 为什么一维不需要显式队列
> 多源 BFS 的本质是"从所有源点同时开始按距离一层层扩散"。一维情况下，"层"退化成只有
> "往左传播"和"往右传播"两个方向：从左到右扫一遍记录"最近一次见到的 2"，就等价于所有
> 源点同时向右扩散一层的效果；再从右到左扫一遍、取两次结果的较小值，就是完整的多源 BFS
> 结果——用两个变量代替了显式的队列结构，常数更小。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：先想清楚"没有 2 时全 -1、没有 1 时输出为空"这两个边界，再写主逻辑。
2. **Part 1 最小可用**：从左到右扫一遍记录 `last_two` 位置，算左侧距离；再从右到左扫一遍算右侧距离，取较小值。
3. **Part 2 叠加**：把所有值为 `2` 的格子同时作为起点入队，做一次标准多源 BFS（因为网格无障碍，BFS 层数就是曼哈顿距离）。
4. **收尾**：`1` 紧邻 `2`（距离1）、`1` 两侧都有 `2`（取较小值）、二维网格行长不一致要报错。

## 4. 代码怎么组织

```
_validate_1d(arr) / _validate_2d(grid)
nearest_two_distances(arr)          # Part 1：两遍线性扫描
nearest_two_distances_grid(grid)    # Part 2：多源 BFS，网格无障碍所以 BFS 距离 = 曼哈顿距离
part1 / part2
```
两个函数不共享代码（维度不同、数据结构不同），但解决的是同一个问题形状——面试里可以
先point出"一维是二维的特化"，再分别实现，避免让面试官以为你在做两道无关的题。

## 5. 核心代码骨架

```python
from collections import deque

def nearest_two_distances(arr):
    # Part 1：两遍扫描——先左到右，再右到左，取较小值
    n = len(arr)
    dist = [float("inf")] * n
    last_two = None
    for i in range(n):
        if arr[i] == 2:
            last_two = i
        elif last_two is not None:
            dist[i] = min(dist[i], i - last_two)
    last_two = None
    for i in range(n - 1, -1, -1):
        if arr[i] == 2:
            last_two = i
        elif last_two is not None:
            dist[i] = min(dist[i], last_two - i)
    return [(-1 if dist[i] == float("inf") else dist[i]) for i in range(n) if arr[i] == 1]

def nearest_two_distances_grid(grid):
    # Part 2：所有 2 同时入队，多源 BFS；网格无障碍，BFS 层数即曼哈顿距离
    rows, cols = len(grid), len(grid[0])
    dist = [[float("inf")] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == float("inf"):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return [(-1 if dist[r][c] == float("inf") else dist[r][c])
            for r in range(rows) for c in range(cols) if grid[r][c] == 1]
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我先确认：没有 2 时所有 1 输出 -1，没有 1 时输出为空，对吗？」
- 写 Part 1 时：「这本质是多源 BFS 在一维上的特化，两遍扫描分别对应'往左传播'和'往右传播'，不需要显式队列。」
- 引出 Part 2 时：「二维的话我会把所有 2 同时入队做标准多源 BFS；因为网格无障碍，BFS 距离就是曼哈顿距离。」

## 7. 常见跑偏（方法层面，3 条）

- 对每个 `1` 单独枚举所有 `2` 算距离取最小（`O(n·k)`），没意识到两遍扫描/多源 BFS 能做到线性。
- 混淆"没有 2"（全部 -1）和"没有 1"（输出为空）这两种不同的空/非空结果。
- 二维网格假设有障碍去写完整的可达性判断，其实题目里网格无障碍，直接 BFS 或计算曼哈顿距离都行。

## 8. 同族题 / 延伸

- 与 LC 542 "01 Matrix"、`pc02`（多源 BFS 到最近设施）是同一族技巧在不同问题上的应用。
- 练习命令：`python3 drill.py start q25`

## 索引行

| [q25_distance_to_nearest_two](q25_distance_to_nearest_two.md) | `../../problems/q25_distance_to_nearest_two/` | OA | "每个点到最近的一批源点的距离"永远可以用多源 BFS 解决；维度低（比如一维）时可以把 BFS 特化成更省常数的两遍扫描，但本质是同一个算法 |
