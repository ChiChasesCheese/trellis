---
id: tlc-number-of-islands-4-followup
node: p1.number-of-islands
type: qa
step: 4
---
## Q
**LC 200 岛屿数量**｜追问

面试官接着问：（1）不能改输入网格？（2）陆地一个一个加进来，每加一个都要立刻回答当前岛屿数（LC 305）？（3）求最大岛屿的面积（LC 695）？（4）全是陆地的网格递归爆栈（`RecursionError`）怎么办？

## A
1. **不改输入**：另开 `visited` 二维布尔数组，判断条件多一项 `not visited[nr][nc]`，空间多 `O(mn)`。
2. **动态加陆地**：每次重新搜索太慢。改用并查集（Union-Find）：新增一格计数加一，与已是陆地的邻居合并，每次合并两个不同的集合计数减一。

```python
def num_islands_ii(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    count, answer = 0, []
    for r, c in positions:
        cell = r * n + c
        if cell not in parent:
            parent[cell] = cell
            count += 1
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                nb = nr * n + nc
                if 0 <= nr < m and 0 <= nc < n and nb in parent:
                    a, b = find(cell), find(nb)
                    if a != b:
                        parent[a] = b
                        count -= 1
        answer.append(count)
    return answer
```

`num_islands_ii(3, 3, [[0,0],[0,1],[1,2],[2,1]])` → `[1, 1, 2, 3]`；重复添加 `[1,2]` 不改变岛数。
3. **最大面积**：让 `sink` 返回沉掉的格数（`1 + 四个方向的返回值之和`），取最大值；`[[1,1,0],[0,1,0],[0,0,1]]` → `3`。
4. **递归爆栈**：最坏深度 `mn`（`9 * 10^4`）超过默认的约 1000。调高 `sys.setrecursionlimit(10**5)`，或把 `sink` 换成显式栈：

```python
def sink_stack(grid: list[list[str]], r0: int, c0: int) -> None:
    grid[r0][c0] = "0"
    stack = [(r0, c0)]
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == "1":
                grid[nr][nc] = "0"
                stack.append((nr, nc))
```

主函数里 `sink(r, c)` 换成 `sink_stack(grid, r, c)`，`300 x 300` 全 `"1"` → `1`。

**Python 提醒**：二维数组别写 `[[False] * cols] * rows`，所有行是同一个列表对象，标一格等于标一整列；要写成 `[[False] * cols for _ in range(rows)]`。
