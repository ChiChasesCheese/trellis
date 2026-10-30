---
id: tlc-tt-longest-zigzag-grid-path-4-followup
node: p4.tt-longest-zigzag-grid-path
type: qa
step: 4
---
## Q
**网格中最长的之字形递增路径**｜追问

最长之字形递增路径（严格递增、水平竖直交替）写完后，面试官接着问：（1）把这条最长路径本身输出出来；（2）如果不要求水平竖直交替，解法怎么变？

## A
1. **输出路径。** 转移时额外记下取到最大值的邻居：`nxt[d][i][j] = (ni, nj)`。填完表后找到最大值所在的 `(d, i, j)`，从它出发沿 `nxt` 走，每走一步方向类型翻转，直到 `nxt` 为空。额外空间 `O(mn)`，回溯 `O(路径长度)`。

```python
H, V = 0, 1
STEPS = (((0, 1), (0, -1)), ((1, 0), (-1, 0)))


def longest_zigzag_with_path(grid: list[list[int]]) -> list[int]:
    m, n = len(grid), len(grid[0])
    dp = [[[1] * n for _ in range(m)] for _ in range(2)]
    nxt: list[list[list[tuple[int, int] | None]]] = [[[None] * n for _ in range(m)] for _ in range(2)]
    for val, i, j in sorted(((grid[i][j], i, j) for i in range(m) for j in range(n)), reverse=True):
        for d in (H, V):
            for di, dj in STEPS[d]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > val and 1 + dp[1 - d][ni][nj] > dp[d][i][j]:
                    dp[d][i][j] = 1 + dp[1 - d][ni][nj]
                    nxt[d][i][j] = (ni, nj)              # 记下取到最大值的邻居
    _, d, i, j = max((dp[d][i][j], d, i, j) for d in (H, V) for i in range(m) for j in range(n))
    path = [grid[i][j]]
    while (step := nxt[d][i][j]) is not None:
        i, j = step
        d = 1 - d                                        # 走完一步，方向类型翻转
        path.append(grid[i][j])
    return path
```

   运行：`[[1,2],[4,3]]` → `[1, 2, 3, 4]`；`[[4,2,1],[1,6,1]]` → `[1, 2, 6]`。
2. **不要求交替。** 去掉 `d` 这一维，`dp[i][j] = 1 + max dp[邻居]`（四个方向、值更大），就是 LC 329 矩阵中的最长递增路径，同样按值排序或拓扑排序填表。

**Python 提醒**：`max` 作用在元组 `(dp, d, i, j)` 上，`dp` 并列时会继续比较 `d, i, j`，结果是确定的；若并列后要比较的位置上是 `None` 和整数混在一起（例如把 `nxt` 放进元组），会抛 `TypeError`，这时改用 `max(..., key=lambda t: t[0])`。
