---
slug: number-of-paths-with-max-score
---
## Q
**LC 1301 最大得分的路径数目**｜Hard

正方形棋盘，从右下角 `S` 出发，每步向上、向左或向左上走一格，到左上角 `E`。数字格加分，`X` 是障碍。求最大得分，以及得到最大得分的路径数（对 `1e9+7` 取模）；到不了返回 `[0, 0]`。

## A
**一句话。** `f[i][j] = (最大得分, 方案数)`：从三个来向取得分最大者，方案数把得分等于最大的来向相加，再加本格分数。

```python
def paths_with_max_score(board):
    MOD = 10 ** 9 + 7
    n = len(board)
    # f[i][j]：从 S 走到 (i, j) 的 (最大得分, 方案数)，-1 不可达
    f = [[(-1, 0)] * (n + 1) for _ in range(n + 1)]
    f[n - 1][n - 1] = (0, 1)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if board[i][j] == "X" or i == j == n - 1:
                continue
            src = [f[i + 1][j], f[i][j + 1],
                   f[i + 1][j + 1]]
            best = max(s for s, _ in src)
            if best < 0:
                continue                   # 三个来向都不可达
            ways = sum(c for s, c in src if s == best) % MOD
            ch = board[i][j]
            gain = 0 if ch == "E" else int(ch)
            f[i][j] = (best + gain, ways)
    s, c = f[0][0]
    return [s, c] if s >= 0 else [0, 0]
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 只保留得分不记方案数：最大得分相同的来向要把方案数相加，得分小的来向方案数不算。
- 用 `0` 表示不可达：得分可以是 `0`（只有 `E`、`S`），要用 `-1` 区分不可达。
- 起点、终点当成数字：`S`、`E` 的分数为 `0`，要单独处理，不能 `int("E")`。

**追问。**
- 为什么多个最优来向的方案数要累加？：路径数是所有同样得分的来源路径数之和，不同来向互不重复。
- 反方向（从 `E` 往 `S` 算）行吗？：可以，起点终点对称，结果相同。

**同模式。** LC 62 不同路径、LC 63 不同路径 II
