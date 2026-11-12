---
slug: pacific-atlantic-water-flow
---
## Q
**LC 417 太平洋大西洋水流问题**｜Medium

水从格子流向上下左右高度小于等于它的邻居；太平洋接上、左边界，大西洋接下、右边界。求既能流到两个海洋的格子。

## A
**一句话。** 反向思考：从两个海洋的边界各做一次 DFS 逆流而上，取两个可达集合的交集。

```python
def pacific_atlantic(heights):
    m, n = len(heights), len(heights[0])

    def reach(starts):
        seen = set()

        def dfs(r, c):
            seen.add((r, c))
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                x, y = r + dx, c + dy
                if (x, y) in seen:
                    continue
                if not (0 <= x < m and 0 <= y < n):
                    continue
                if heights[x][y] >= heights[r][c]:
                    dfs(x, y)   # 逆流：走不矮的邻居

        for r, c in starts:
            if (r, c) not in seen:
                dfs(r, c)
        return seen

    pac = reach([(0, c) for c in range(n)]
                + [(r, 0) for r in range(1, m)])
    atl = reach([(m-1, c) for c in range(n)]
                + [(r, n-1) for r in range(m-1)])
    return [list(p) for p in pac & atl]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 逆流比较写成严格 `>`：等高也能流，`[[1,1],[1,1]]` 只得 `[[0,1],[1,0]]`，应为四格。
- 比较方向写反（用 `<=`）：从海洋出发是逆流，要走向更高或相等的格子。
- 对每个格子单独 DFS：`4·10^4` 格各搜一遍会超时。

**追问。**
- 递归太深怎么办？：改成多源 BFS，两个海洋的边界分别入队，其余逻辑不变。
- 只要个数？：`len(pac & atl)`。

**同模式。** LC 130 被围绕的区域、LC 1020 飞地的数量、LC 542 01 矩阵、LC 286 墙与门
