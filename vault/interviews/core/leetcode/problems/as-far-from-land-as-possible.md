---
slug: as-far-from-land-as-possible
---
## Q
**LC 1162 地图分析**｜Medium

`n x n` 网格里 `0` 是海洋，`1` 是陆地。求海洋格到最近陆地的曼哈顿距离的最大值，全是陆地或全是海洋返回 `-1`。

## A
**一句话。** 所有陆地同时入队做多源 BFS，最后一层的层数就是答案。

```python
def max_distance(grid):
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    q = deque((r, c) for r in range(n) for c in range(n)
              if grid[r][c])
    for r, c in q:
        dist[r][c] = 0
    if not q or len(q) == n * n:    # 全海或全陆
        return -1
    far = 0
    while q:
        r, c = q.popleft()
        for x, y in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            if 0 <= x < n and 0 <= y < n and dist[x][y] < 0:
                dist[x][y] = far = dist[r][c] + 1
                q.append((x, y))
    return far
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 只从一块陆地出发：得到的是到那块陆地的距离，示例 1 从左上角出发得 `3`，应为 `2`。
- 漏掉全陆地 / 全海洋：`[[1,1],[1,1]]` 和 `[[0,0],[0,0]]` 会返回 `0`，应为 `-1`。
- 出队时才标记距离：同一格会被多次入队。

**追问。**
- 要返回那个格子？：记下最后一次赋值的 `(x, y)`。
- 八方向（切比雪夫距离）？：邻居改成 8 个，BFS 不变。

**同模式。** LC 542 01 矩阵、LC 994 腐烂的橘子、LC 286 墙与门、LC 934 最短的桥
