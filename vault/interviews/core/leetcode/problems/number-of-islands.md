---
slug: number-of-islands
---
## Q
**LC 200 岛屿数量**｜Medium

`'1'` 是陆地、`'0'` 是水的二维网格，数上下左右相连的陆地块（岛屿）有几个。

## A
**一句话。** 扫描网格，每遇到一块未处理的陆地就计数加一，再用 DFS 把整座岛沉成 `'0'`。

**图解。** 行优先扫描，遇到新陆地计数加一，再用 DFS 把整座岛沉掉。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 140">
<rect x="20" y="16" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="34.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="48" y="16" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="34.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="76" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="44" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="62.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="48" y="44" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="62.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="76" y="44" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="44" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="44" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="48" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="76" y="72" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="90.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="104" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="48" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="76" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="100" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="118.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="132" y="100" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="118.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="176" y="36" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">格中数字：第几座岛</text>
<text x="176" y="60" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色：扫到它时计数 +1</text>
<text x="176" y="84" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">浅色：被这次 DFS 沉掉</text>
<text x="176" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="600">答案 3</text>
</svg>

```python
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        if not (0 <= r < rows and 0 <= c < cols):
            return
        if grid[r][c] != "1":
            return
        grid[r][c] = "0"       # 先沉再搜，同一格不会重复进入
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只向右、向下搜：U 形岛 `[["1","0","1"],["1","1","1"]]` 会数成 `2`，应为 `1`。
- 比较写成整数 `1`：格子是字符串 `"1"`，结果恒为 `0`。
- 整片陆地时递归深达 `mn`：CPython 抛 `RecursionError`，需调高上限或改显式栈。

**追问。**
- 不许改输入网格？：另开 `visited` 集合。
- 陆地逐个加入、每次都要答岛屿数？：并查集，新增陆地计数加一，每合并一对不同集合减一。

**同模式。** LC 695 岛屿的最大面积、LC 130 被围绕的区域、LC 694 不同岛屿的数量、LC 305 岛屿数量 II
