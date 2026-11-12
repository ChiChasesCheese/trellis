---
slug: 01-matrix
---
## Q
**LC 542 01 矩阵**｜Medium

对 `0/1` 矩阵 `mat`，求每个格子到最近的 `0` 的距离（上下左右每步为 `1`）。

## A
**一句话。** 所有 `0` 同时入队做多源 BFS，每格第一次被访问时的层数就是它到最近 `0` 的距离。

```python
def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    q = deque()
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))     # 所有 0 是第 0 层
    while q:
        i, j = q.popleft()
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < m and 0 <= y < n and dist[x][y] < 0:
                dist[x][y] = dist[i][j] + 1   # 入队即标记
                q.append((x, y))
    return dist
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 对每个 `1` 单独跑 BFS：`O((mn)^2)`，`mn = 10^4` 时超时。
- 只从一个 `0` 出发：`[[0,1,1,1,0]]` 得 `[0,1,2,3,4]`，应为 `[0,1,2,1,0]`。
- 出队时才标记：同一格被多个邻居重复入队。

**追问。**
- 不用队列怎么做？：两趟 DP，左上到右下取 `min(上, 左) + 1`，再右下到左上取 `min(下, 右) + 1`。
- 8 邻接呢？：方向表加 4 个，距离变成切比雪夫距离。

**同模式。** LC 994 腐烂的橘子、LC 286 墙与门、LC 1162 地图分析、LC 1091 二进制矩阵中的最短路径
