---
id: cc-performance-numeric-arrays-matmul-loop-order
node: performance.numeric-arrays
type: qa
---
## Q
Write matrix multiply `C = A · B`. All six orders of the three loops give the same answer and O(n^3) work. Why is `i-k-j` much faster than the textbook `i-j-k`?

## A
**Memory is row-major. In `i-j-k` the inner loop reads `B[k][j]` down a column, jumping a whole row each step; in `i-k-j` it reads one row of `B` and one row of `C` left to right, so every cache line fetched is fully used.**

```python
def matmul_ikj(A, B):
    n, p = len(A), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        Ci = C[i]
        for k, a in enumerate(A[i]):
            if a == 0:                  # free win when A is sparse
                continue
            Bk = B[k]                   # one row of B, read left to right
            for j in range(p):
                Ci[j] += a * Bk[j]
    return C
```

- **Cache line.** The CPU fetches 64 bytes at a time (eight float64). A row uses all eight; a column uses one, and at n = 1024 the next row is 8 KB away.
- **Measured.** C, n = 1024, `-O2`, one Apple-Silicon core: `i-j-k` 1.4 s, `i-k-j` 0.11 s. Pure Python, n = 200: 0.19 s vs 0.13 s — there lists hold pointers, so the gain is mostly from hoisting `B[k]` and `C[i]`.
- **Bonus.** `if a == 0: continue` skips a whole row: the trick for sparse `A`.
- **Complexity.** O(n·m·p) time, O(n·p) for `C`.

**Follow-up: "B is too big for the cache."** Tile the loops so small blocks stay in cache; in Python, use `numpy` (`A @ B`).

## Q zh
写出矩阵乘法 `C = A · B`。三层循环的六种顺序答案相同、工作量都是 O(n^3)，为什么 `i-k-j` 比教科书上的 `i-j-k` 快得多？

## A zh
**内存按行连续存放（行主序）。`i-j-k` 的内层循环沿一列读 `B[k][j]`，每步跳过一整行；`i-k-j` 的内层循环从左到右读 `B` 的一行和 `C` 的一行，取进来的每条缓存行都被用满。**

```python
def matmul_ikj(A, B):
    n, p = len(A), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        Ci = C[i]
        for k, a in enumerate(A[i]):
            if a == 0:                  # free win when A is sparse
                continue
            Bk = B[k]                   # one row of B, read left to right
            for j in range(p):
                Ci[j] += a * Bk[j]
    return C
```

- **缓存行（cache line）。** CPU 一次取 64 字节，即 8 个 float64。沿行读 8 个全用上；沿列只用 1 个，n = 1024 时下一行在 8 KB 之外。
- **实测。** C 语言、n = 1024、`-O2`、Apple Silicon 单核：`i-j-k` 1.4 秒，`i-k-j` 0.11 秒。纯 Python、n = 200：0.19 秒对 0.13 秒——列表里存的是指针，收益主要来自把 `B[k]` 和 `C[i]` 提到循环外。
- **附带好处。** `if a == 0: continue` 跳过一整行：稀疏 `A` 的技巧。
- **复杂度。** O(n·m·p) 时间，`C` 占 O(n·p)。

**追问：「B 太大装不进缓存。」** 对循环分块（tiling），让小块留在缓存里；Python 里直接用 `numpy`（`A @ B`）。
