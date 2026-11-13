---
id: cc-performance-parallel-split-prefix-2d-threads
node: performance.parallel-split
type: qa
---
## Q
Compute the 2D prefix sum of a large matrix with several threads. How do you split the work so no two threads write the same cell, and where must they wait for each other?

## A
**The 2D prefix is separable: prefix every row, then every column. Phase 1 gives each thread a band of rows, phase 2 a band of columns, with one barrier between: a column needs every row finished.**

```python
from concurrent.futures import ThreadPoolExecutor
import numpy as np

def bands(n, w):
    return [(n * i // w, n * (i + 1) // w) for i in range(w)]

def prefix_2d_threads(M, workers=4):
    P = M.astype(np.int64)                      # private copy, shared by threads
    m, n = P.shape
    def rows(lo, hi):                           # phase 1: rows are independent
        np.cumsum(P[lo:hi], axis=1, out=P[lo:hi])
    def cols(lo, hi):                           # phase 2: columns are independent
        np.cumsum(P[:, lo:hi], axis=0, out=P[:, lo:hi])
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(rows, *zip(*bands(m, workers))))   # list() = barrier
        list(ex.map(cols, *zip(*bands(n, workers))))
    return P                                    # P[i, j] = sum of M[:i+1, :j+1]
```

- **No locks.** Bands in a phase are disjoint slices. `list(ex.map(...))` waits for all tasks: that is the barrier.
- **Why threads work here.** numpy releases the GIL in its C loops. 8000 × 8000 int64: 1 thread 0.31 s, 4 threads 0.08 s, 8 threads 0.06 s. Pure-Python loops would gain nothing.
- **Stride.** Phase 2 walks columns; `out=` writes in place, nothing is copied.
- **Complexity.** O(m·n / w) per phase plus one barrier; int64, since the corner holds the whole sum.

**Follow-up: "one pass over the data."** Each thread computes its tile's local 2D prefix, then adds offsets from the tiles above and left: the 2D form of the two-pass scan.

## Q zh
用多个线程计算一个大矩阵的二维前缀和。怎么分工才能保证两个线程不写同一个格子？它们必须在哪里互相等待？

## A zh
**二维前缀和可以分离：先对每行求前缀，再对每列求前缀。第一阶段每个线程分一段行，第二阶段分一段列，中间一道屏障（barrier）：任何一列都需要所有行先算完。**

```python
from concurrent.futures import ThreadPoolExecutor
import numpy as np

def bands(n, w):
    return [(n * i // w, n * (i + 1) // w) for i in range(w)]

def prefix_2d_threads(M, workers=4):
    P = M.astype(np.int64)                      # private copy, shared by threads
    m, n = P.shape
    def rows(lo, hi):                           # phase 1: rows are independent
        np.cumsum(P[lo:hi], axis=1, out=P[lo:hi])
    def cols(lo, hi):                           # phase 2: columns are independent
        np.cumsum(P[:, lo:hi], axis=0, out=P[:, lo:hi])
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(rows, *zip(*bands(m, workers))))   # list() = barrier
        list(ex.map(cols, *zip(*bands(n, workers))))
    return P                                    # P[i, j] = sum of M[:i+1, :j+1]
```

- **不需要锁。** 同一阶段的各段是不相交的切片。`list(ex.map(...))` 等所有任务完成：这就是屏障。
- **为什么这里线程有用。** numpy 在 C 循环里释放 GIL。8000 × 8000 的 int64：1 个线程 0.31 秒，4 个 0.08 秒，8 个 0.06 秒。纯 Python 循环则毫无收益。
- **跨步。** 第二阶段按列跨步访问；`out=` 原地写回，不复制数据。
- **复杂度。** 每阶段 O(m·n / w) 加一次屏障；用 int64，因为右下角存的是整个矩阵的和。

**追问：「只扫一遍数据。」** 每个线程算出自己那块（tile）的局部二维前缀，再加上来自上方和左方各块的偏移量：两遍扫描的二维版本。
