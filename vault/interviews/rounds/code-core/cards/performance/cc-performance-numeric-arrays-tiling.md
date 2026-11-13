---
id: cc-performance-numeric-arrays-tiling
node: performance.numeric-arrays
type: qa
---
## Q
What is blocking (tiling) a matrix multiply? Write it, say how you pick the tile size, and when it pays off a lot.

## A
**Cut the matrices into T × T tiles and multiply tile by tile. A tile in cache is reused T times before eviction, so slow-memory traffic drops about T-fold.**

```python
def matmul_tiled(A, B, T=32):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i0 in range(0, n, T):
        for k0 in range(0, m, T):
            for j0 in range(0, p, T):
                # one T x T tile of C += tile of A @ tile of B
                for i in range(i0, min(i0 + T, n)):
                    Ci, Ai = C[i], A[i]
                    for k in range(k0, min(k0 + T, m)):
                        a, Bk = Ai[k], B[k]
                        for j in range(j0, min(j0 + T, p)):
                            Ci[j] += a * Bk[j]
    return C
```

- **Why.** One tile step reads 2·T² numbers and does T³ multiply-adds: T/2 operations per number fetched.
- **Picking T.** Three tiles must fit the target cache: 3 × 8 bytes × T² ≤ 32 KB (a common x86 L1) gives T ≤ 36, so T = 32 for float64. Then measure.
- **When it pays.** Little on a big-cache desktop CPU (C, n = 2048: 0.78 s vs 0.87 s for `i-k-j`). Decisive where fast memory is small and hand-managed: GPU shared memory, an accelerator's on-chip SRAM (small fast memory beside the compute units).
- **Complexity.** O(n^3) operations; traffic about O(n^3 / T).

**Follow-up: "parallelise it."** Each worker owns its own `C` tiles, so no locks.

## Q zh
什么是矩阵乘法的分块（blocking / tiling）？写出来，说明怎么选块大小，什么时候收益很大。

## A zh
**把矩阵切成 T × T 的块，按块相乘。缓存里的一个块被重复使用 T 次才被挤出，所以访问慢速内存的流量大约降到 1/T。**

```python
def matmul_tiled(A, B, T=32):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i0 in range(0, n, T):
        for k0 in range(0, m, T):
            for j0 in range(0, p, T):
                # one T x T tile of C += tile of A @ tile of B
                for i in range(i0, min(i0 + T, n)):
                    Ci, Ai = C[i], A[i]
                    for k in range(k0, min(k0 + T, m)):
                        a, Bk = Ai[k], B[k]
                        for j in range(j0, min(j0 + T, p)):
                            Ci[j] += a * Bk[j]
    return C
```

- **原因。** 一次块运算读 2·T² 个数，做 T³ 次乘加：每取一个数做 T/2 次运算。
- **选 T。** 三个块要放进目标缓存：3 × 8 字节 × T² ≤ 32 KB（x86 常见的 L1），得 T ≤ 36，float64 取 T = 32。再实测。
- **什么时候值。** 在缓存大的桌面 CPU 上收益小（C 语言 n = 2048：0.78 秒对 `i-k-j` 的 0.87 秒）。真正决定性的是快速内存小且手动管理的硬件：GPU 共享内存（shared memory）、加速器的片上 SRAM（紧挨计算单元的小而快的内存）。
- **复杂度。** 运算 O(n^3)；内存流量约 O(n^3 / T)。

**追问：「把它并行化。」** 每个 worker 只写自己的 `C` 块，所以不需要锁。
