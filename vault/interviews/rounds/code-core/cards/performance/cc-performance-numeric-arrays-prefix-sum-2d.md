---
id: cc-performance-numeric-arrays-prefix-sum-2d
node: performance.numeric-arrays
type: qa
---
## Q
An m × n integer grid gets 10^5 queries "sum of the rectangle from (r1, c1) to (r2, c2)". Build a structure that answers each in O(1).

## A
**A 2D prefix sum: `P[i][j]` = sum of all cells above and left of (i, j), padded with a zero row and column. A rectangle is four lookups by inclusion–exclusion.**

```python
def build_prefix(M):
    m, n = len(M), len(M[0])
    # P[i][j] = sum of M[0:i][0:j]; the extra zero row/col kills edge cases
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += M[i][j]
            P[i + 1][j + 1] = P[i][j + 1] + row_sum
    return P

def rect_sum(P, r1, c1, r2, c2):
    # inclusive corners (r1, c1) .. (r2, c2)
    return (P[r2 + 1][c2 + 1] - P[r1][c2 + 1]
            - P[r2 + 1][c1] + P[r1][c1])
```

- **Formula.** Big rectangle from the origin, minus the strip above, minus the strip to the left, plus the corner removed twice.
- **Check.** `[[1,2,3],[4,5,6],[7,8,9]]`: `P[3][3] = 45`; bottom-right 2 × 2 is `45 - 6 - 12 + 1 = 28` = 5 + 6 + 8 + 9.
- **Padding** removes every edge `if`.
- **Overflow.** 10^4 × 10^4 values up to 10^6 sum to 10^14, past 2^31: use 64-bit in C, Java or numpy.
- **Complexity.** Build O(m·n) time and memory; query O(1).

**Follow-ups.** "Cells change" → 2D Fenwick tree, O(log m · log n) per update and query. "Build it with threads" → prefix every row independently, then every column, with one barrier between.

## Q zh
一个 m × n 的整数网格要回答 10^5 次「从 (r1, c1) 到 (r2, c2) 的矩形之和」。建一个结构，让每次查询 O(1)。

## A zh
**二维前缀和：`P[i][j]` = (i, j) 左上方所有格子之和，外补一行一列 0。矩形和用容斥原理查四次。**

```python
def build_prefix(M):
    m, n = len(M), len(M[0])
    # P[i][j] = sum of M[0:i][0:j]; the extra zero row/col kills edge cases
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += M[i][j]
            P[i + 1][j + 1] = P[i][j + 1] + row_sum
    return P

def rect_sum(P, r1, c1, r2, c2):
    # inclusive corners (r1, c1) .. (r2, c2)
    return (P[r2 + 1][c2 + 1] - P[r1][c2 + 1]
            - P[r2 + 1][c1] + P[r1][c1])
```

- **公式。** 从原点开始的大矩形，减去上方那条，减去左边那条，再加回被减了两次的角。
- **验证。** `[[1,2,3],[4,5,6],[7,8,9]]`：`P[3][3] = 45`；右下角 2 × 2 是 `45 - 6 - 12 + 1 = 28` = 5 + 6 + 8 + 9。
- **补零**去掉了所有边界 `if`。
- **溢出。** 10^4 × 10^4 个不超过 10^6 的值之和是 10^14，超过 2^31：C、Java、numpy 里用 64 位。
- **复杂度。** 构建 O(m·n) 时间和内存；查询 O(1)。

**追问。**「格子会变」→ 二维树状数组（Fenwick tree），更新和查询都是 O(log m · log n)。「用多线程构建」→ 先各行独立求前缀，再各列独立求前缀，中间一道屏障（barrier）。
