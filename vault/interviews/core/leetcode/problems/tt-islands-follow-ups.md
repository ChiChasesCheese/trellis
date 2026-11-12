---
slug: tt-islands-follow-ups
---
## Q
**岛屿数量及其追问集合**｜Hard

`m x n` 的 0/1 网格，`1` 是陆地。依次求：（1）岛屿数，不能改原网格；（2）形状不同的岛屿数（只算平移）；（3）旋转、翻转后相同也算同一种。

## A
**一句话。** 递归 DFS 洪水填充（flood fill）产出每座岛的格子，形状签名取「减去最小坐标后排序」，旋转翻转则对 8 种变换取最小签名。

```python
D = ((1, 0), (-1, 0), (0, 1), (0, -1))

def components(grid):
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]   # 不改原网格
    def dfs(x, y, cells):
        seen[x][y] = True
        cells.append((x, y))
        for dx, dy in D:
            a, b = x + dx, y + dy
            if (0 <= a < m and 0 <= b < n
                    and grid[a][b] and not seen[a][b]):
                dfs(a, b, cells)
    for r in range(m):
        for c in range(n):
            if grid[r][c] and not seen[r][c]:
                cells = []
                dfs(r, c, cells)
                yield cells

def num_islands(grid):
    return sum(1 for _ in components(grid))

def norm(pts):               # 平移归一化后的签名
    x0, y0 = min(pts)
    return tuple(sorted((x - x0, y - y0) for x, y in pts))

def distinct(grid):
    return len({norm(c) for c in components(grid)})

# 8 种变换 = 4 次旋转 × 是否翻转
T = [lambda x, y: (x, y), lambda x, y: (x, -y),
     lambda x, y: (-x, y), lambda x, y: (-x, -y),
     lambda x, y: (y, x), lambda x, y: (y, -x),
     lambda x, y: (-y, x), lambda x, y: (-y, -x)]

def distinct_ii(grid):
    shapes = set()
    for c in components(grid):
        forms = [norm([f(x, y) for x, y in c]) for f in T]
        shapes.add(min(forms))
    return len(shapes)
```

**复杂度。** 时间 `O(mn log mn)`，空间 `O(mn)`。

**易错点。**
- 签名没做平移归一化：用绝对坐标，两座同形岛会被当成不同。
- 只做 4 种旋转、漏了翻转：S 形和 Z 形应算同一种。
- 访问数组写成 `[[False] * n] * m`：所有行是同一个列表，标上一格等于标上整列。

**追问。**
- 递归深度爆了怎么办？：全 `1` 的网格深度可达 `9 * 10^4`，调大 `setrecursionlimit` 或改显式栈。
- 地图太大放不进内存？：分块并查集，再合并块边界上相邻的陆地。

**同模式。** LC 200 岛屿数量、LC 694 不同岛屿的数量、LC 711 不同岛屿的数量 II、LC 695 岛屿的最大面积
