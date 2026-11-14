---
slug: amazon-flip-zero-minimax-distance
---
## Q
**翻一个 0 使最远距离最小**｜Hard

0/1 网格，必须把一个 `0` 改成 `1`。之后每个 `0` 到最近 `1` 的曼哈顿距离取最大，求这个最大值的最小可能值。

## A
**一句话。** 多源 BFS 求每格到旧 `1` 的距离 `d`；二分答案 `R`：`d > R` 的格子都要落在新 `1` 的半径 `R` 内，换成 `u = r + c`、`v = r - c` 后菱形变成矩形，扫一遍 `0` 格看有没有落进两个区间的交。

```python
def min_max_distance(grid):
    m, n, INF = len(grid), len(grid[0]), float("inf")
    d = [[0 if v else INF for v in row] for row in grid]
    q = deque((i, j) for i in range(m) for j in range(n)
              if grid[i][j])
    while q:                  # 多源 BFS：到旧 1 的距离
        i, j = q.popleft()
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < m and 0 <= y < n and d[x][y] == INF:
                d[x][y] = d[i][j] + 1
                q.append((x, y))
    zeros = [(i, j) for i in range(m) for j in range(n)
             if not grid[i][j]]

    def ok(R):                # 一个新 1 能盖住所有 d > R 的格？
        far = [(i, j) for i, j in zeros if d[i][j] > R]
        if not far:
            return True
        us = [i + j for i, j in far]
        vs = [i - j for i, j in far]
        return any(max(us) - R <= i + j <= min(us) + R
                   and max(vs) - R <= i - j <= min(vs) + R
                   for i, j in zeros)

    lo, hi = 0, m + n
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(mn log(m + n))`，空间 `O(mn)`。

**易错点。**
- 只看 `u`、`v` 区间交非空就返回 `True`：交里的点可能 `u`、`v` 奇偶不同不是整点，或不是 `0` 格，要扫真实的 `0` 格。
- 只检查 `u` 一个区间：曼哈顿距离 `<= R` 等价于 `|Δu| <= R` 且 `|Δv| <= R`，两个都要。

**追问。**
- 有墙挡路？：距离不再是曼哈顿，坐标变换失效；只能对候选点各跑 BFS，或在规模小时枚举。
- 可以翻 `k` 个？：变成网格上的 `k` 中心问题，一般是 NP 难，问清规模再定枚举或近似。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1162 地图分析、LC 1131 绝对值表达式的最大值、LC 2812 找出最安全路径
