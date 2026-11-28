---
id: lct-learn-dp-2-1
node: dp.2.1
type: qa
step: 1
---
## Q
**动态规划 › 网格图 DP › 基础**｜学习卡

套路是什么？

## A
**一句话。** 只能向下或向右时，`(i, j)` 只来自上方和左方：按行遍历，状态是「走到这一格」，多开一圈哨兵省去边界特判。

下图：`(i, j)` 只能从上方或左方走来；多开一圈 `inf` 哨兵，起点从上方拿到 0。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="20" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="40.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="60" y="20" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="100" y="20" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="120.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="140" y="20" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="20" y="48" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="40.0" y="66.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="60" y="48" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="66.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="100" y="48" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120.0" y="66.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="140" y="48" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="66.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="20" y="76" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="40.0" y="94.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="60" y="76" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80.0" y="94.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="100" y="76" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120.0" y="94.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<rect x="140" y="76" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="94.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">6</text>
<rect x="20" y="104" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="40.0" y="122.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inf</text>
<rect x="60" y="104" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="122.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">6</text>
<rect x="100" y="104" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="122.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">8</text>
<rect x="140" y="104" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="122.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7</text>
<line x1="120.0" y1="70.0" x2="120.0" y2="78.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,78.0 117.0,71.7 123.0,71.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="90.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="98.0,90.0 91.7,93.0 91.7,87.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="200" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">grid = [[1,3,1],</text>
<text x="200" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,5,1],[4,2,1]]</text>
<text x="200" y="84" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f = min(上, 左) + g</text>
<text x="200" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 = min(4, 2) + 5</text>
<text x="200" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">外圈 inf 是哨兵</text>
</svg>

```python
def min_path_sum(g):
    m, n = len(g), len(g[0])
    # f[i+1][j+1]：走到 (i, j) 的最小和；多一圈 inf 哨兵
    f = [[inf] * (n + 1) for _ in range(m + 1)]
    f[0][1] = 0                  # 让起点从上方哨兵拿到 0
    for i in range(m):
        for j in range(n):
            up, left = f[i][j + 1], f[i + 1][j]
            f[i + 1][j + 1] = min(up, left) + g[i][j]
    return f[m][n]
```

**要点。**
- 为什么对？：到 `(i, j)` 的路径最后一步只能来自上或左，行优先遍历时这两格已算好；哨兵取 `inf` 保证越界来源不会被选中。
- LC 62、63 怎么改？：`min(..) + g` 换成「上 + 左」，哨兵换成 `0`、起点哨兵 `f[0][1] = 1`；LC 63 障碍格直接保持 `0`。
- LC 120 怎么改？：自底向上：`f[i][j] = 自己 + min(下方, 右下方)`，最底行就是初值，答案是顶点；不需要哨兵。

**易错点。**
- 边界没初始化：留着的 `0` 被当成免费来源，`[[1],[2],[3]]` 得 `0`，应为 `6`。
- LC 63 照搬 LC 62 把首行首列全设 `1`：`[[0,1,0]]` 得 `1`，应为 `0`，障碍之后不可达。
- 每步贪心走较小的邻格：`[[1,3,1],[1,5,1],[4,2,1]]` 得 `9`，应为 `7`。

**对应题目。** LC 62 不同路径、LC 63 不同路径 II、LC 64 最小路径和、LC 120 三角形最小路径和
