---
id: tlc-python-dp-space-compression-1-when-shrink
node: python.dp-space-compression
type: qa
step: 1
---
## Q
**DP 降维｜什么时候二维表可以缩小**

二维 DP 的表什么时候可以缩小？以不同路径（LC 62）为例，判断的依据是什么？

## A
先写完整的二维表，再看转移公式里 `dp[i][j]` 读了哪些格子，**只看它们的行下标**。

```python
m, n = 3, 4
dp = [[1] * n for _ in range(m)]            # dp[i][j]：从左上角走到 (i, j) 的路径数
for i in range(1, m):
    for j in range(1, n):
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1]   # 读上方 (i-1, j) 和左边 (i, j-1)
print(dp)   # [[1, 1, 1, 1], [1, 2, 3, 4], [1, 3, 6, 10]]
```

```
dp[i-1][j-1]   dp[i-1][j]
dp[i][j-1]     dp[i][j]  <- 正在算
```

- 读到的行下标只有 `i-1` 和 `i`：算完第 `i` 行后，第 `i-1` 行再也不会被读，可以丢掉。只留上一行和本行即可（下一张卡），甚至合成一行（再下一张）。
- 一旦要读 `dp[i-2]`、`dp[0]` 或任意行（区间 DP 枚举分割点 `k`，读 `dp[i][k]` 和 `dp[k+1][j]`），就不能丢行。
- 压缩只省空间，时间不变：`O(mn)` 时间，空间从 `O(mn)` 降到 `O(n)`。
- 顺序：先写二维表把答案写对，再压缩。
