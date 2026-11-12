---
slug: shortest-path-in-a-grid-with-obstacles-elimination
---
## Q
**LC 1293 网格中的最短路径**｜Hard

`0` 空 `1` 障碍的网格，最多可消除 `k` 个障碍，求从左上走到右下的最少步数，走不到返回 `-1`。

## A
**一句话。** 带状态 BFS：状态是 `(行, 列, 剩余消除数)`，每格只记见过的最大剩余数。

```python
def shortest_path(grid, k):
    m, n = len(grid), len(grid[0])
    if k >= m + n - 3:        # 直走最多穿 m+n-3 堵墙
        return m + n - 2
    best = [[-1] * n for _ in range(m)]
    best[0][0] = k
    q = deque([(0, 0, k)])
    steps = 0
    while q:
        steps += 1
        for _ in range(len(q)):
            i, j, left = q.popleft()
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                x, y = i + dx, j + dy
                if not (0 <= x < m and 0 <= y < n):
                    continue
                nl = left - grid[x][y]
                if nl > best[x][y]:    # 剩余更多才值得再来
                    if (x, y) == (m-1, n-1):
                        return steps
                    best[x][y] = nl
                    q.append((x, y, nl))
    return -1
```

**复杂度。** 时间 `O(mn·min(k, m+n))`，空间 `O(mn)`。

**易错点。**
- `visited` 只按格子记：先到但剩余少的状态会挡掉后到但剩余多的，把有解判成 `-1`。
- 出队时才判终点：多走一层，步数偏大；入队时就判断。

**追问。**
- 状态集合 `(i,j,left)` 去重行不行？：行，最直观，只是状态多一个 `k` 因子。
- 怎么还原路径？：记每个状态的前驱 `(i,j,left)`，到终点后回溯。

**同模式。** LC 1091 二进制矩阵中的最短路径、LC 864 获取所有钥匙的最短路径、LC 752 打开转盘锁、LC 127 单词接龙
