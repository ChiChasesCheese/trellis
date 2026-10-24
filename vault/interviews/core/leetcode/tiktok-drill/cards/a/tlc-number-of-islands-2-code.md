---
id: tlc-number-of-islands-2-code
node: a.number-of-islands
type: qa
step: 2
---
## Q
**LC 200 岛屿数量**｜写出 Python 实现

`grid` 是 `m x n` 的字符网格，元素是 `'1'`（陆地）或 `'0'`（水），`1 <= m, n <= 300`。返回岛屿数量，相邻只算上下左右。要求不用递归（最坏要走 `9 * 10^4` 格）。

## A
**思路。** 逐格扫描，遇到 `'1'` 就计数加一，再用显式栈把这座岛的所有陆地改成 `'0'`。入栈时就标记，保证每格只入栈一次。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != "1":
                continue
            count += 1                                  # 找到一座新岛：把它整座沉掉
            grid[r0][c0] = "0"
            stack = [(r0, c0)]                          # 显式栈，避免 300x300 全是陆地时递归爆栈
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"              # 入栈时就标记，同一格不会入栈两次
                        stack.append((nr, nc))
    return count
```

运行：示例一 → `1`，示例二 → `3`；`[["0"]]` → `0`，`[["1"]]` → `1`；`300 x 300` 全 `"1"` → `1`，一座"蛇形"的岛（`300 x 300`，一整条蜿蜒的通路）→ `1`，都不触发递归限制。

**复杂度。** 时间 `O(mn)`：每格被扫描一次，被标记和弹出至多各一次；空间最坏 `O(mn)`（全是陆地时栈里可能积压很多格）。

**写法要点。** 方向用元组遍历 `for nr, nc in ((r + 1, c), ...)`，比 `dr, dc` 两个列表再 `zip` 直观；`0 <= nr < rows` 是链式比较，一行表达边界；原地把 `"1"` 改成 `"0"` 省掉 `visited` 数组，但会改输入；`r0, c0` 和 `r, c` 分开命名，避免内层循环覆盖外层的扫描位置。
