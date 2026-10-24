---
id: tlc-number-of-islands-4-followup
node: a.number-of-islands
type: qa
step: 4
---
## Q
**LC 200 岛屿数量**｜追问

面试官接着问：（1）不允许修改输入网格？（2）陆地一个一个加进来，每加一个都要立刻回答当前岛屿数（LC 305）？（3）求最大岛屿的面积（LC 695）？

## A
1. **不改输入**：另开 `visited = [[False] * cols for _ in range(rows)]`（或把坐标放进 `set`），判断条件多一项 `not visited[nr][nc]`，其余不变。空间多 `O(mn)`。
2. **动态加陆地**：每次重新搜索是 `O(mn)` 一次，太慢。改用并查集（Union-Find）：新增一格先令计数加一，再与四个已是陆地的邻居合并，每次合并两个不同的集合计数减一。

```python
def num_islands_ii(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]              # 路径减半
            x = parent[x]
        return x

    count, answer = 0, []
    for r, c in positions:
        cell = r * n + c
        if cell not in parent:                         # 同一格重复添加不改变岛数
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

`num_islands_ii(3, 3, [[0,0],[0,1],[1,2],[2,1]])` → `[1, 1, 2, 3]`；把 `[1,2]` 重复添加 `[[0,0],[0,1],[1,2],[1,2]]` → `[1, 1, 2, 2]`。每次操作近似 `O(1)`（反阿克曼函数）。
3. **最大面积**：沿用上面的栈搜索，每找到一座新岛就数出栈次数作为面积，取最大值；`[[1,1,0],[0,1,0],[0,0,1]]` → `3`。

**Python 提醒**：二维数组别写 `[[False] * cols] * rows`，所有行是同一个列表对象，标一格等于标一整列；要写成 `[[False] * cols for _ in range(rows)]`。
