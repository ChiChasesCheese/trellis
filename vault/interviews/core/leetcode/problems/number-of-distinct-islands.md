---
slug: number-of-distinct-islands
---
## Q
**LC 694 不同岛屿的数量**｜Medium

0/1 网格里上下左右相连的 `1` 是岛屿。统计形状不同的岛屿数，只允许平移重合，不能旋转或翻转。

## A
**一句话。** 搜出每座岛的格子，减去岛的起点得到平移不变的相对坐标集合，放进 `set` 去重。

```python
def num_distinct_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    shapes = set()
    DIRS = (1, 0), (-1, 0), (0, 1), (0, -1)
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != 1 or seen[r0][c0]:
                continue
            seen[r0][c0] = True   # 行优先第一格，是这座岛的固定原点
            stack = [(r0, c0)]
            cells = []
            while stack:
                r, c = stack.pop()
                cells.append((r - r0, c - c0))
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            shapes.add(frozenset(cells))
    return len(shapes)
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只比较格子数：横向三连和拐角三格大小都是 `3`，会被当成同一种形状。
- 用绝对坐标当签名：两个 2x2 方块位置不同，会被数成 `2` 座。
- 原点取搜索遇到的任意格：同一形状会得到不同签名，必须取固定参照格。

**追问。**
- 旋转和翻转也算相同（LC 711）？：生成 8 种变换，各自平移归一后取最小的当签名。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 711 不同岛屿的数量 II、LC 1905 统计子岛屿
