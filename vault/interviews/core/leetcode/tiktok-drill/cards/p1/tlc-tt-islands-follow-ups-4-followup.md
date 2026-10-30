---
id: tlc-tt-islands-follow-ups-4-followup
node: p1.tt-islands-follow-ups
type: qa
step: 4
---
## Q
**岛屿数量及其追问集合**｜追问

`m x n` 的 0/1 网格，上下左右相连的 `1` 是一座岛，已有递归 DFS 数岛屿、不改网格。面试官接着问：（0）蛇形岛让递归爆栈怎么办？（1）要求「边界」，是格子数还是周长？（2）8 方向相连怎么改？（3）求最大岛面积、以及「最多把一个 `0` 变成 `1`」后的最大岛？（4）地图大到内存放不下，或者一行一行流式读入？

## A
0. **递归爆栈**：全 `1` 的 `300 x 300` 网格 DFS 深度可达 `9 * 10^4`，超过默认上限约 `1000`。改成显式栈，入栈时就标记：
```python
def components(grid: list[list[int]]) -> Iterator[list[tuple[int, int]]]:
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            seen[r][c] = True
            cells, stack = [], [(r, c)]
            while stack:                                    # 显式栈代替递归
                x, y = stack.pop()
                cells.append((x, y))
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and not seen[nx][ny]:
                        seen[nx][ny] = True                 # 入栈时就标记，避免重复入栈
                        stack.append((nx, ny))
            yield cells
```
   也可以用 `sys.setrecursionlimit` 调大上限。
1. **边界要先问清**。边界格子数：陆地格中至少有一个邻居是水或越界的格子。周长：`4 * 陆地格数 - 2 * 相邻陆地对数`，每对相邻的陆地格各让周长少 1 条边，一遍扫描 `O(mn)`。
2. **8 方向**：`DIRS` 加上四个对角方向，其余不变；岛屿数通常变少。
3. **最大岛面积**：`max(map(len, components(grid)))`。**最大人工岛**（LC 827）：先给每座岛编号并记面积，再扫每个 `0`，把四个邻居中**不同编号**的岛面积相加再加 `1`，用集合去重编号，取最大；全是 `1` 时直接返回 `m * n`。
4. **内存放不下**：分块，每块内用并查集；块边界上相邻的两格陆地，把各自集合合并，最后数根的个数。**流式**：逐行读，只保存上一行每格的标签，上方、左方都是水就新建一座岛，两边标签不同就合并并把总数减 1；内存 `O(n)`。

**Python 提醒**：把 `visited` 和 `grid` 合并成一个字符串/元组网格时，字符串不可变，不能 `row[c] = '0'`；`copy.deepcopy(grid)` 对 `300 x 300` 很慢，需要副本时用 `[row[:] for row in grid]`。
