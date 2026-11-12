---
slug: making-a-large-island
---
## Q
**LC 827 最大人工岛**｜Hard

`n×n` 的 0/1 矩阵最多把一个 `0` 变成 `1`，求变后最大岛屿面积（四连通）。

## A
**一句话。** 先给每座岛编号并记面积，再枚举每个 `0`，把四周不同岛的面积相加再加 `1`。

```python
def largest_island(grid):
    n = len(grid)
    label = [[0] * n for _ in range(n)]   # 岛编号，0 = 水/未编号
    size = {}                             # 编号 -> 面积

    def nbrs(i, j):
        for a, b in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    def dfs(i, j, tag):
        label[i][j] = tag
        area = 1
        for a, b in nbrs(i, j):
            if grid[a][b] == 1 and label[a][b] == 0:
                area += dfs(a, b, tag)
        return area

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                size[tag] = dfs(i, j, tag)
    best = max(size.values(), default=0)  # 不翻 / 没有 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                # 四邻岛编号去重
                tags = {label[a][b] for a, b in nbrs(i, j)}
                area = 1 + sum(size.get(t, 0) for t in tags)
                best = max(best, area)
    return best
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 邻居岛不去重：`[[1,1],[1,0]]` 加成 `3+3+1=7`，应为 `4`。
- `best` 不用面积初始化：全 `1` 的 `[[1,1],[1,1]]` 会返回 `0`，应为 `4`。
- 递归过深：全 `1` 的 `500×500` 深度可达 `2.5×10^5`，要调大递归上限或改显式栈。

**追问。**
- 最多翻 `k` 格？：不再是邻居面积相加，要在翻转预算下做搜索，复杂度上升。
- 要输出翻哪一格？：取最大时记下 `(i, j)`。

**同模式。** LC 695 岛屿的最大面积、LC 200 岛屿数量、LC 934 最短的桥、LC 1020 飞地的数量
