---
slug: amazon-forbidden-turn-grid
---
## Q
**只能直行或左转的网格最短路**｜Medium

网格里 `0` 是空地、`1` 是墙，每步走一格；新方向只能和上一步相同或左转 90°（不能右转、掉头），第一步方向任选。求起点到终点的最少步数，不可达返回 `-1`。

## A
**一句话。** 方向进状态：在 `(行, 列, 朝向)` 上 BFS，只生成直行和左转两种转移，第一次出队到终点时的步数就是答案。

```python
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 北东南西

def min_steps(grid, start, target):
    m, n = len(grid), len(grid[0])
    sr, sc = start
    q = deque((sr, sc, h, 0) for h in range(4))
    seen = {(sr, sc, h) for h in range(4)}
    while q:
        r, c, h, d = q.popleft()
        if (r, c) == tuple(target):
            return d
        for nh in (h, (h - 1) % 4):   # 直行或左转
            x, y = r + DIRS[nh][0], c + DIRS[nh][1]
            if (0 <= x < m and 0 <= y < n
                    and grid[x][y] == 0
                    and (x, y, nh) not in seen):
                seen.add((x, y, nh))  # 按三元组去重
                q.append((x, y, nh, d + 1))
    return -1
```

**复杂度。** 时间 `O(mn)`（`4mn` 个状态，每个 2 条边），空间 `O(mn)`。

**易错点。**
- 只按 `(行, 列)` 去重：从另一个方向进同一格后能走的路不同，会把唯一的可行路线剪掉。
- 左转写成 `(h + 1) % 4`：在北东南西的顺序里那是右转。

**追问。**
- 每格的禁转规则不同？：状态不变，转移时查 `banned[x][y]` 里有没有 `(入向, 出向)`。
- 转弯有代价，或最多转 `K` 次？：有代价用 0-1 BFS 或 Dijkstra；限次数就把已转次数也放进状态。

**同模式。** LC 994 腐烂的橘子、LC 1293 网格中的最短路径、LC 490 迷宫、LC 1263 推箱子
