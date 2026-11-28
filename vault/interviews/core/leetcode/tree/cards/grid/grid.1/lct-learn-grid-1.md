---
id: lct-learn-grid-1
node: grid.1
type: qa
step: 1
---
## Q
**网格图 › 网格图 DFS**｜学习卡

套路是什么？

## A
**一句话。** 网格是隐式的图：格子是点、相邻格子是边；DFS 从一个格子出发把整个连通块一次吃掉，数块数、块大小、是否碰边界都是一次 DFS 加一个标记。

下图：格子是点、相邻格子是边；一次 DFS 吃掉一整个连通块。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="20" y="20" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="54" y="20" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="71" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="88" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="122" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="156" y="20" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="173" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="20" y="54" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="54" y="54" width="34" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="71" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="88" y="54" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="122" y="54" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="139" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="156" y="54" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="173" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="20" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="54" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="88" y="88" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="122" y="88" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="139" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="156" y="88" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="173" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="20" y="122" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="37" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="54" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="88" y="122" width="34" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="122" y="122" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="139" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="156" y="122" width="34" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="173" y="143" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<line x1="43" y1="37" x2="63" y2="37" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="63.0,37.0 56.7,40.0 56.7,34.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="37" y1="43" x2="37" y2="63" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="37.0,63.0 34.0,56.7 40.0,56.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="200" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从一个 1 出发 DFS</text>
<text x="200" y="50" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">吃掉整个连通块</text>
<text x="200" y="76" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">访问过就置 0</text>
<text x="200" y="92" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">再向四邻展开</text>
<text x="200" y="120" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">启动次数 = 岛屿数</text>
<text x="200" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回值 = 块大小</text>
</svg>

```python
def max_area(grid):                 # LC 695；LC 200 数启动次数
    m, n = len(grid), len(grid[0])

    def dfs(i, j):                  # 返回这个连通块的大小
        if not (0 <= i < m and 0 <= j < n and grid[i][j]):
            return 0                # 出界、水或已访问
        grid[i][j] = 0              # 置 0 即标记，再向四邻展开
        return (1 + dfs(i - 1, j) + dfs(i + 1, j)
                + dfs(i, j - 1) + dfs(i, j + 1))

    return max(dfs(i, j)
               for i in range(m) for j in range(n))
```

**要点。**
- 为什么对？：每个格子只在第一次被访问时展开，之后被标记挡住，总共 `O(mn)`；从任一格启动都吃掉整块。
- LC 1254 封闭岛屿、LC 130 被围绕的区域、LC 417 太平洋大西洋怎么改？：反着从边界出发做 DFS，把“与边界相连”的格子标出来，剩下的就是答案（417 要从两个大洋分别出发，取交集，只走向不低于当前的格子）。
- LC 827 最大人工岛怎么改？：先给每块编号并记大小，再对每个 `0` 把四邻不同编号的块大小相加再加 `1`。
- LC 305 岛屿数量 II 怎么改？：格子逐个变陆地，是动态连通性，用并查集。

**易错点。**
- 先取值后判出界：`[[1,0,1]]` 应得 `2`，Python 的负下标不报错，会读到另一端的格子。
- 标记放在递归之后：任意两个相邻的 `1`，如 `[[1,1]]`，会互相递归到栈溢出。
- 733 新旧颜色相同：`image = [[0,0,0],[0,0,0]]`、`color = 0` 应原样返回，不特判会无限递归。

**对应题目。** LC 3619 总价值可以被 K 整除的岛屿数目、LC 733 图像渲染、LC 827 最大人工岛、LC 695 岛屿的最大面积、LC 529 扫雷游戏、LC 1254 统计封闭岛屿的数目、LC 305 岛屿数量 II、LC 200 岛屿数量、LC 417 太平洋大西洋水流问题、LC 489 扫地机器人、LC 130 被围绕的区域
