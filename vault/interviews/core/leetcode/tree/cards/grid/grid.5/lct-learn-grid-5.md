---
id: lct-learn-grid-5
node: grid.5
type: qa
step: 1
---
## Q
**网格图 › 综合应用**｜学习卡

套路是什么？

## A
**一句话。** 比较岛屿形状：DFS 收集每个岛的格子，全部减去起点（行优先第一个格子）得到与位置无关的相对坐标，装进可哈希的集合去重。

下图：LC 694，两个岛位置不同，减去各自起点后得到同一个相对坐标集合。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="15" y="15" width="34" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="32" y="34" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0,0</text>
<rect x="49" y="15" width="34" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="66" y="34" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0,1</text>
<rect x="83" y="15" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="117" y="15" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="15" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="185" y="15" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="219" y="15" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="15" y="45" width="34" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="32" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1,0</text>
<rect x="49" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="83" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="117" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="185" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="219" y="45" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="15" y="75" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="49" y="75" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="83" y="75" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="117" y="75" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="75" width="34" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="168" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">0,0</text>
<rect x="185" y="75" width="34" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="202" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">0,1</text>
<rect x="219" y="75" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="15" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="49" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="83" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="117" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="105" width="34" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="168" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1,0</text>
<rect x="185" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="219" y="105" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">每格减去起点：两岛的相对坐标集合相同 → 同一形状</text>
</svg>

```python
def num_distinct_islands(grid):     # LC 694：只允许平移
    m, n = len(grid), len(grid[0])
    shapes = set()

    def dfs(i, j, i0, j0, cells):
        if not (0 <= i < m and 0 <= j < n and grid[i][j]):
            return
        grid[i][j] = 0              # 置 0 即标记已访问
        cells.append((i - i0, j - j0))      # 相对起点的坐标
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            dfs(x, y, i0, j0, cells)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                cells = []
                dfs(i, j, i, j, cells)
                shapes.add(frozenset(cells))    # 形状与位置无关
    return len(shapes)
```

**要点。**
- 为什么对？：行优先扫描遇到的第一个格子是岛上最靠上、同行最靠左的点，平移后同形状的岛得到同一个相对坐标集合。
- LC 711 不同岛屿的数量 II 怎么改？：每个岛生成 8 种变换（4 个旋转，各带翻转），每种先排序再减去字典序最小的点，取其中最小的元组当规范形。

**易错点。**
- 用绝对坐标：两个 `2×2` 方块 `[[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` 应得 `1`，不减原点会得到 `2`。
- 711 只做旋转漏了翻转：S 形和 Z 形互为镜像，应算同一种。
- 711 变换后不排序、不重新平移：点的顺序依赖 DFS 顺序，同形的岛会得到不同的元组。

**对应题目。** LC 711 不同岛屿的数量 II、LC 694 不同岛屿的数量
