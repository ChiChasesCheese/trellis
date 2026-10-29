---
id: tlc-swim-in-rising-water-5-alt
node: a.swim-in-rising-water
type: qa
step: 5
---
## Q
**LC 778 水位上升的泳池中游泳**｜另一种解法

不用堆，还有什么写法能解 `n x n`（`n <= 50`，高度是 `0..n^2-1` 的一个排列）的「水位上升泳池」？它的复杂度是多少，什么时候该选它而不是 Dijkstra？

## A
**并查集，水位从低到高一格格点亮。** 因为高度是 `0..n^2-1` 的排列，先建一张 `pos[h]` 表，记下高度为 `h` 的格子坐标。然后让水位 `t` 从 `0` 涨到 `n^2 - 1`：点亮 `pos[t]`，把它与所有高度不超过 `t` 的邻格合并；一旦起点和终点同根，当前 `t` 就是答案。

```python
def swim_dsu(grid: list[list[int]]) -> int:
    n = len(grid)
    pos = [(0, 0)] * (n * n)
    for i, row in enumerate(grid):
        for j, h in enumerate(row):
            pos[h] = (i, j)                        # 高度互不相同且是 0..n²-1 的排列
    parent = list(range(n * n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for t, (x, y) in enumerate(pos):               # 水位从 0 涨到 n²-1：每涨一格就把它和已淹没的邻居并起来
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] <= t:
                parent[find(x * n + y)] = find(nx * n + ny)
        if find(0) == find(n * n - 1):
            return t
    return -1
```

示例 `[[0,2],[1,3]]` → `3`，`5 x 5` 的示例 → `16`，`[[3,0],[1,2]]` → `3`，与堆版结果一致。

**复杂度。** 时间 `O(n^2 α(n^2))`，近似线性（没有排序，也没有堆）；空间 `O(n^2)`。

**另一条路：二分答案 + BFS。** 对水位 `t` 二分，`check(t)` 用 BFS 只走高度 `<= t` 的格子，看能否到终点；`O(n^2 log n)`，代码最短，但每次查询都要整张图重新搜。

**怎么选。**
- 单次查询、高度任意：Dijkstra，不依赖「排列」这个特殊条件。
- 高度恰好是排列、要最快：并查集，没有对数因子。
- 有很多组起点终点查询：并查集（离线）更容易扩展。
- 想用最少的代码快速写对：二分加 BFS。
