---
id: tlc-number-of-distinct-islands-2-code
node: a.number-of-distinct-islands
type: qa
step: 2
---
## Q
**LC 694 不同岛屿的数量**｜写出 Python 实现

`grid` 是 `m x n` 的 0/1 网格，`1 <= m, n <= 50`，岛屿是四连通的 `1`。返回形状不同的岛屿数量，只允许用平移判断两座岛是否相同。

## A
**思路。** 行优先扫描，遇到未访问的 `1` 就以它为原点，用显式栈收集这座岛所有格子相对原点的偏移，存成 `frozenset` 放进集合；最后返回集合大小。

```python
def num_distinct_islands(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    shapes: set[frozenset[tuple[int, int]]] = set()
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != 1 or seen[r0][c0]:
                continue
            # (r0, c0) 是行优先扫描遇到的第一格，也就是这座岛最靠上、同行最靠左的格子
            seen[r0][c0] = True
            stack = [(r0, c0)]
            cells: list[tuple[int, int]] = []
            while stack:
                r, c = stack.pop()
                cells.append((r - r0, c - c0))     # 相对起点的偏移 = 平移不变量
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            shapes.add(frozenset(cells))           # 无序的格子集合：与遍历顺序无关
    return len(shapes)
```

运行：`[[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` → `1`；`[[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]` → `3`；`[[0]]` → `0`；`[[1,0,1]]` → `1`；`[[1,1,0],[0,1,1]]` → `1`；`50 x 50` 全是 `1` → `1`。

**复杂度。** 时间 `O(mn)`；空间 `O(mn)`（`seen`、栈和所有签名）。

**写法要点。** `frozenset` 可哈希，普通 `set` 不行，所以才能放进另一个集合；集合比较与遍历顺序无关，不需要对偏移排序；类型标注 `set[frozenset[tuple[int, int]]]` 直接写出签名的结构；这里的 `seen` 单独存放，不改输入网格。
