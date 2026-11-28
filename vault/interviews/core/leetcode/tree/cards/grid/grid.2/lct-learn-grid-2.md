---
id: lct-learn-grid-2
node: grid.2
type: qa
step: 1
---
## Q
**网格图 › 网格图 BFS**｜学习卡

套路是什么？

## A
**一句话。** 每步代价相同的网格最短路用 BFS：像扔石头的涟漪一圈圈外扩，先到的一定更近；多个起点就全部当作第 0 圈一起入队。

下图：多源 BFS，格子里写的是到最近起点的步数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="20" y="20" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="54" y="20" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="71" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="88" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="122" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="156" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="173" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="20" y="54" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="37" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="54" y="54" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="88" y="54" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="54" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="156" y="54" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="173" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="20" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="54" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="88" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="122" y="88" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="139" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="156" y="88" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="173" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="20" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="54" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="88" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="156" y="122" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="173" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="200" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两个起点都是第 0 圈</text>
<text x="200" y="50" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一起入队</text>
<text x="200" y="76" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">涟漪一圈圈外扩</text>
<text x="200" y="92" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">格内数字 = 圈数</text>
<text x="200" y="120" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入队时就标记</text>
<text x="200" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis = -1 即未访问</text>
</svg>

```python
def bfs_grid(grid, sources):        # 多源 BFS，层数即步数
    m, n = len(grid), len(grid[0])
    dis = [[-1] * n for _ in range(m)]  # -1 同时当未访问
    q = deque(sources)
    for i, j in sources:
        dis[i][j] = 0               # 所有起点是第 0 圈
    while q:
        i, j = q.popleft()
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if (0 <= x < m and 0 <= y < n
                    and grid[x][y] != 0 and dis[x][y] < 0):
                dis[x][y] = dis[i][j] + 1   # 入队时就标记
                q.append((x, y))
    return dis
```

**要点。**
- 为什么对？：队列里的距离非降，先出队的格子距离最小，第一次到达某格时就是它的最短距离。
- LC 994 腐烂的橘子、LC 542、LC 286、LC 1162 怎么改？：起点分别是所有烂橘子、所有 `0`、所有门、所有陆地；994 取新鲜橘子的最大距离，有不可达的返回 `-1`。
- LC 1293 带障碍消除怎么改？：点变成 `(i, j, 剩余次数)`，访问集合也多一维。
- LC 505 迷宫 II、LC 499 迷宫 III 怎么改？：球滚到墙才停，一步多格，代价不等，用 Dijkstra。

**易错点。**
- 出队才标记已访问：同一格会重复入队，务必入队时标记。
- 994 忽略孤立的新鲜橘子：`[[2,1,1],[0,1,1],[1,0,1]]` 应得 `-1`，只取最大距离会得到 `4`。
- 1926 把入口当出口：`maze = [[".","+"]]`、入口 `[0,0]` 应得 `-1`。

**对应题目。** LC 542 01 矩阵、LC 1162 地图分析、LC 1926 迷宫中离入口最近的出口、LC 994 腐烂的橘子、LC 934 最短的桥、LC 317 离建筑物最近的距离、LC 1293 网格中的最短路径、LC 1091 二进制矩阵中的最短路径、LC 909 蛇梯棋、LC 505 迷宫 II、LC 499 迷宫 III、LC 286 Walls and Gates
