---
slug: island-perimeter
---
## Q
**LC 463 岛屿的周长**｜Easy

`0/1` 网格中恰有一个岛屿（无湖），求它的周长。

## A
**一句话。** 每块陆地贡献 4 条边，每有一对上下或左右相邻的陆地就少 2；扫描时只看上方和左方，避免重复。

**图解。** 7 块陆地、6 对相邻：`7×4 − 6×2 = 16`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 212">
<rect x="26" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="56" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="116" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="26" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="56" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="86" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="116" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="26" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="56" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="86" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="116" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="26" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="56" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="86" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="116" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="158" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">7 块陆地，每块 4 条边</text>
<text x="16" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6 对相邻陆地，每对少 2</text>
<text x="16" y="194" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">28 − 12 = 16</text>
</svg>

```python
def island_perimeter(grid):
    m, n = len(grid), len(grid[0])
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                ans += 4
                if i and grid[i - 1][j]:
                    ans -= 2   # 与上方共用一条边
                if j and grid[i][j - 1]:
                    ans -= 2   # 与左方共用一条边
    return ans
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 共用边只减 1：这条边两侧的格子各少一条，共减 2。
- 四个方向都检查再减 2：每对会被算两次，要么只看上、左，要么每个方向减 1。

**追问。**
- DFS 写法？：从陆地出发，每走到水或出界就算一条边，走到陆地就继续搜。
- 有湖呢？：湖的边也算周长，计数法不受影响；DFS 写法则要注意湖边同样是「碰到水」。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 827 最大人工岛
