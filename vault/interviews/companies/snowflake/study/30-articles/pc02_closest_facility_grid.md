# pc02 · Closest Facility Grid：练的是"多源 BFS，以及 tie-break 不能交给队列顺序"

> [!tldr]
> - Part 1、Part 2 有来源题面（1p3a 题库公开预览 + fastprep "High Frequency"）；**Part 3 加墙体是 (reconstructed)**
> - 这题考的是：每个工位到最近卫生间的步数（多源 BFS），再说出是哪个卫生间（字典序最小），再加墙
> - 三步套路：所有卫生间同时入队 → 按"整层"扩展，同层内对同一格子的多个来源显式比较 → 墙格子直接跳过
> - 最值得带走的一个模式：**并列时的赢家必须由显式比较决定**，不能由"谁先入队"决定——换一种写法答案就变了

## 1. 题目在说什么（人话版）

办公室网格里有卫生间 `B`、工位 `D`、空地 `.`（Part 3 还有墙 `#`）。对每个工位（按行优先顺序）算走到最近卫生间要几步（只能上下左右）。Part 2 还要说出是哪个卫生间，距离相同选坐标最小的。Part 3 墙不能穿。

小例子（Part 1）：
```
. . B
. D .
. . . D
工位 (1,1) 到 (0,2)：2 步；工位 (2,3)：3 步
```

## 2. 读题：把文字变成模型

- **实体**：格子、卫生间（多个起点）、工位（查询点）、墙。
- **输出**：按工位的行优先顺序输出距离（Part 2/3 还有卫生间坐标）；够不到输出 `-1` / `(-1,-1)`。
- **状态**：`dist[r][c]`、`source[r][c]`（最近卫生间）、当前层 frontier。
- **一句话建模**：这是一个 **"以所有卫生间为同时起点的网格 BFS"**，Part 2 在每层结算时比较来源。

> [!note] 为什么不对每个工位单独 BFS
> 1000×1000 网格、工位很多时，每个工位一次 BFS 是 O(格子数 × 工位数)。反过来从所有卫生间一起出发，一次 BFS 覆盖所有格子，O(格子数)。

## 3. 下笔顺序

1. **问清**：只能 4 方向？没有卫生间输出什么？工位顺序是行优先？
2. **Part 1**：所有 `B` 入 frontier，`dist=0`；逐层扩展，未访问的邻居 `dist=d+1`。最后按行优先读工位的 dist。
3. **Part 2**：把"单队列"改成"整层处理"：本层所有格子先把邻居的**候选来源**记在 `claims[邻居]` 里，同一个邻居有多个候选时取坐标最小的；本层结束再统一写 `dist` 与 `source`。
4. **Part 3**：扩展时遇到 `#` 跳过。用"曼哈顿距离很近但被墙挡住"的例子自测。
5. **收尾**：没有卫生间、工位被墙隔绝、网格为空。

## 4. 代码怎么组织

```
_bfs_with_source(grid, blocked_char) -> (dist, source)   # 三个 part 共用
_desks(grid)                                              # 行优先工位列表
nearest_bathroom_distances / _with_location / _with_obstacles
part1..part3                                              # 解析与格式化
```

## 5. 核心代码骨架

```python
def _bfs_with_source(grid, blocked=None):
    m, n = len(grid), len(grid[0]) if grid else 0
    dist = [[-1] * n for _ in range(m)]; src = [[None] * n for _ in range(m)]
    frontier = sorted((r, c) for r in range(m) for c in range(n) if grid[r][c] == "B")
    for r, c in frontier:
        dist[r][c], src[r][c] = 0, (r, c)
    d = 0
    while frontier:
        claims = {}                                   # 邻居 -> 最小候选来源
        for r, c in frontier:
            for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1 and grid[nr][nc] != blocked:
                    if (nr, nc) not in claims or src[r][c] < claims[(nr, nc)]:
                        claims[(nr, nc)] = src[r][c]
        if not claims:
            break
        d += 1
        for (nr, nc), s in claims.items():
            dist[nr][nc], src[nr][nc] = d, s
        frontier = list(claims)
    return dist, src
```

## 6. 每个 part 叠加什么

| Part | 改动 |
|---|---|
| 1 | 多源 BFS 求距离 |
| 2 | 按层结算 + 同层候选来源显式取最小 |
| 3 | 扩展时跳过墙 |

## 7. 常见坑

- 对每个工位单独 BFS（超时）。
- 单队列多源 BFS 下，tie 的赢家取决于入队顺序——测试专门构造两个卫生间等距的格子。
- 用曼哈顿距离代替 BFS 距离：无墙时碰巧对，Part 3 的绕墙例子会戳破。
- 工位本身不是障碍：BFS 可以穿过工位格子。
- 递归 DFS：1000×1000 爆栈，而且 DFS 不给最短距离。

## 8. 追问怎么接

1. **网格巨大、只有少数工位要查？** 反过来从工位做双向 BFS 或 A*（曼哈顿启发式）。
2. **卫生间有容量上限，要给每个工位分配一个？** 变成最小费用匹配 / 分配问题，不再是纯 BFS。
3. **网格动态变化（新开一个卫生间）？** 从新卫生间做一次 BFS，只更新距离变小的格子。
4. **不同格子通行代价不同？** 多源 Dijkstra。

## 9. 自测清单

- [ ] 写出多源 BFS 初始化（所有源同时 dist=0）
- [ ] 构造一个"两个卫生间等距"的格子，说出为什么单队列会不确定
- [ ] 构造一个"曼哈顿近但被墙挡住"的例子

## 相关题与 skills

S05 图 BFS。相关：`pc04` / `q10`（BFS + 路径重建与字典序）、`sd17` Geolocation Search（系统设计版的"最近设施"）。
