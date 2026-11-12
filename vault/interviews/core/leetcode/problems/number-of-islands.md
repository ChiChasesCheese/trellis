---
slug: number-of-islands
---
## Q
**LC 200 岛屿数量**｜Medium

`'1'` 是陆地、`'0'` 是水的二维网格，数上下左右相连的陆地块（岛屿）有几个。

## A
**一句话。** 扫描网格，每遇到一块未处理的陆地就计数加一，再用 DFS 把整座岛沉成 `'0'`。

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
