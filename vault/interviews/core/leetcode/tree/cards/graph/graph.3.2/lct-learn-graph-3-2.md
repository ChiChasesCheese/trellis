---
id: lct-learn-graph-3-2
node: graph.3.2
type: qa
step: 1
---
## Q
**图论算法 › 最短路 › 全源最短路：Floyd 算法**｜学习卡

套路是什么？

## A
**一句话。** 三重循环，`k` 放最外层：允许经过的中转点依次扩大到 `0..k`，`f[i][j] = min(f[i][j], f[i][k] + f[k][j])`，`O(n^3)` 得到任意两点的最短路。

下图：经过中转点 `k` 更短就更新 `f[i][j]`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<line x1="60.7" y1="92.5" x2="139.3" y2="37.5" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="139.3,37.5 135.8,43.6 132.4,38.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="160.7" y1="37.5" x2="239.3" y2="92.5" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="239.3,92.5 232.4,91.3 235.8,86.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<circle cx="50" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">i</text>
<circle cx="150" cy="30" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="150" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k</text>
<circle cx="250" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">j</text>
<line x1="64" y1="100" x2="236" y2="100" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="236.0,100.0 229.7,103.0 229.7,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="150" y="118" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[i][j]</text>
<text x="88" y="58" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i][k]</text>
<text x="212" y="58" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[k][j]</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">k 最外层：允许的中转点依次扩大到 0..k</text>
</svg>

```python
def floyd(n, edges):
    f = [[inf] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0                  # 自己到自己是 0
    for x, y, w in edges:
        f[x][y] = min(f[x][y], w)    # 重边取小
        f[y][x] = min(f[y][x], w)    # 有向图去掉这行
    for k in range(n):               # 中转点必须在最外层
        for i in range(n):
            for j in range(n):
                f[i][j] = min(f[i][j], f[i][k] + f[k][j])
    return f
```

**要点。**
- 为什么对？：`f[k][i][j]` 表示只允许经过前 `k` 个点中转的最短路，要么不经过点 `k`，要么经过一次且两段都只用前 `k - 1` 个点；滚动成二维后顺序仍成立。
- LC 1462 怎么改？：边权看成「可达」，把 `min / +` 换成 `or / and`，得到传递闭包，之后每次查询 `O(1)`；也可用拓扑序加位集。

**易错点。**
- 循环顺序写成 `i, j, k`：`k` 不在最外层会漏掉需要多次中转的路径。
- 不连通的点：用 `inf` 而不是 `-1`，否则 `min` 会把 `-1` 当最短。
- 自环或重边：初始化时没取最小，`0→1` 有权 `5` 和权 `2` 两条边应取 `2`。

**对应题目。** LC 1462 课程表 IV
