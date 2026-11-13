---
id: cc-performance-parallel-split-gil-threads-vs-processes
node: performance.parallel-split
type: qa
---
## Q
You split a pure-Python dot product across 4 threads and it gets no faster. Why? Rewrite it to really run in parallel, and say when even that loses.

## A
**CPython's GIL (global interpreter lock) lets one thread run bytecode at a time: threads overlap waiting, not arithmetic. Use processes, each with its own interpreter.**

```python
from concurrent.futures import ProcessPoolExecutor
import os

def chunk_bounds(n, k):
    # k nearly equal [lo, hi) ranges; sizes differ by at most 1
    return [(n * i // k, n * (i + 1) // k) for i in range(k)]

def partial_dot(args):
    a, b = args                       # the chunk itself is pickled over
    return sum(x * y for x, y in zip(a, b))

def parallel_dot(a, b, workers=os.cpu_count()):
    k = min(workers, len(a)) or 1
    jobs = [(a[lo:hi], b[lo:hi]) for lo, hi in chunk_bounds(len(a), k)]
    with ProcessPoolExecutor(max_workers=k) as ex:
        return sum(ex.map(partial_dot, jobs))   # reduce partial results
```

- **Measured** (12-core Apple Silicon, Python 3.14, 4 workers, each given only its index range): `sqrt(i) * sin(i)` over 8 · 10^6 values — serial 0.34 s, threads 0.37 s, processes 0.17 s.
- **When processes lose.** Dot of 4 · 10^6 floats with slices pickled to workers: serial 0.07 s, processes 0.21 s. Shipping the data cost more than the multiplies.
- **Merge.** `ex.map` keeps submission order, so float partials always add in the same order.
- **Complexity.** O(n / w) per worker, O(w) merge, plus start-up and O(n) pickling.

**Follow-up: "avoid the copy."** Pass `(lo, hi)` and load inside the worker; `multiprocessing.shared_memory`; or numpy, whose loops release the GIL so threads scale. Free-threaded builds (`python3.14t`) drop the GIL.

## Q zh
你把一个纯 Python 的点积分给 4 个线程，结果一点没变快。为什么？改写成真正并行的版本，并说明什么时候连它也会输。

## A zh
**CPython 的 GIL（全局解释器锁）让同一时刻只有一个线程执行字节码：线程能重叠的是等待，不是算术。改用进程，每个进程有自己的解释器。**

```python
from concurrent.futures import ProcessPoolExecutor
import os

def chunk_bounds(n, k):
    # k nearly equal [lo, hi) ranges; sizes differ by at most 1
    return [(n * i // k, n * (i + 1) // k) for i in range(k)]

def partial_dot(args):
    a, b = args                       # the chunk itself is pickled over
    return sum(x * y for x, y in zip(a, b))

def parallel_dot(a, b, workers=os.cpu_count()):
    k = min(workers, len(a)) or 1
    jobs = [(a[lo:hi], b[lo:hi]) for lo, hi in chunk_bounds(len(a), k)]
    with ProcessPoolExecutor(max_workers=k) as ex:
        return sum(ex.map(partial_dot, jobs))   # reduce partial results
```

- **实测**（12 核 Apple Silicon，Python 3.14，4 个 worker，每个只收到自己的下标区间）：对 8 · 10^6 个值求 `sqrt(i) * sin(i)`——串行 0.34 秒，线程 0.37 秒，进程 0.17 秒。
- **进程什么时候输。** 4 · 10^6 个浮点数的点积，切片 pickle 发给 worker：串行 0.07 秒，进程 0.21 秒。发送数据比乘法本身还贵。
- **合并。** `ex.map` 保持提交顺序，所以浮点部分和总是按同一顺序相加。
- **复杂度。** 每个 worker O(n / w)，合并 O(w)，另加进程启动和 O(n) 的 pickle 开销。

**追问：「避免复制。」** 只传 `(lo, hi)`，在 worker 里加载数据；用 `multiprocessing.shared_memory`；或用 numpy，它的循环释放 GIL，线程就能加速。自由线程构建（free-threaded，`python3.14t`）去掉了 GIL。
