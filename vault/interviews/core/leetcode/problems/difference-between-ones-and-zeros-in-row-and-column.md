---
slug: difference-between-ones-and-zeros-in-row-and-column
---
## Q
**LC 2482 行和列中一和零的差值**｜Medium

`m x n` 的 0/1 矩阵 `grid`。构造同样大小的矩阵 `diff`：`diff[i][j] = 第 i 行的 1 的个数 + 第 j 列的 1 的个数 - 第 i 行的 0 的个数 - 第 j 列的 0 的个数`。

## A
**一句话。** 先数每行每列的 `1` 的个数 `r`、`c`，行里 `0` 的个数是 `n - r`，列里是 `m - c`，所以 `diff = 2(r + c) - m - n`。

```python
def ones_minus_zeros(grid):
    m, n = len(grid), len(grid[0])
    rows = [sum(r) for r in grid]
    cols = [sum(c) for c in zip(*grid)]
    return [[2 * (rows[i] + cols[j]) - m - n
             for j in range(n)] for i in range(m)]
```

**复杂度。** 时间 `O(mn)`，空间 `O(m + n)`。

**易错点。**
- 对每个格重新求行列和：`O(mn(m + n))`，预处理一次即可。
- 把 `0` 的个数当成 `n - r` 算反：行里 `0` 的个数用列数 `n`，列里用行数 `m`。

**追问。**
- 也要避免两次遍历？：行和列和各需一次扫描，已是线性。

**同模式。** LC 1267 统计参与通信的服务器、LC 1582 二进制矩阵中的特殊位置、LC 3128 直角三角形
