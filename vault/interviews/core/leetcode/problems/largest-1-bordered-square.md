---
slug: largest-1-bordered-square
---
## Q
**LC 1139 最大的以 1 为边界的正方形**｜Medium

`0/1` 矩阵 `grid`，求最大的正方形子网格，要求它的**四条边**上的格子全是 `1`（内部随意），返回其面积，没有返回 `0`。

## A
**一句话。** 预处理每格向左、向上的连续 `1` 个数；枚举右下角，边长从大到小试，只需检查对应的上边和左边是否也够长。

```python
def largest_1_bordered_square(grid):
    m, n = len(grid), len(grid[0])
    left = [[0] * (n + 1) for _ in range(m + 1)]   # 向左连续 1
    up = [[0] * (n + 1) for _ in range(m + 1)]     # 向上连续 1
    best = 0
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if not grid[r - 1][c - 1]:
                continue
            left[r][c] = left[r][c - 1] + 1
            up[r][c] = up[r - 1][c] + 1
            k = min(left[r][c], up[r][c])
            while k > best:               # 边长从大到小试
                # 上边 (r-k+1 行) 向左要有 k，左边向上要有 k
                if (left[r - k + 1][c] >= k
                        and up[r][c - k + 1] >= k):
                    best = k
                    break
                k -= 1
    return best * best
```

**复杂度。** 时间 `O(mn · min(m, n))`，空间 `O(mn)`。

**易错点。**
- 只检查右下角的两条边：正方形还有上边和左边，要靠另一个角 `left`、`up` 的值确认。
- 边长从小到大试：要从大到小，找到就停，并只试比当前 `best` 更大的边长。
- 返回边长：题目要面积，最后要平方。

**追问。**
- 和「最大正方形」（LC 221）的区别？：那题内部也要全 `1`，用 `min(三邻)+1`；这题只看边界，要连续长度。
- 能更快吗？：上界是 `min(m, n)`，每个格子最多试这么多次，已是常用做法。

**同模式。** LC 221 最大正方形、LC 1277 统计全为 1 的正方形子矩阵、LC 1504 统计全 1 子矩形
