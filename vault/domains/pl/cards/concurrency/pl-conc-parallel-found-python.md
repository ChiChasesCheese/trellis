---
id: pl-conc-parallel-found-python
node: concurrency.parallelism
type: qa
step: 5
---
## Q
Python 做数据并行有哪几条路？NumPy 的向量化和 `multiprocessing` / `ProcessPoolExecutor` 各是什么，怎么选？

## A
纯 Python 循环既慢又受 GIL 限制，数据并行靠“把工作交给能并行的东西”。

**1. NumPy 向量化（单进程）**：NumPy 的数组在内存里是连续的原生数值，操作（`np.sqrt(x) * np.sin(x)`）由编译好的 C 内核执行：没有解释开销，能用 SIMD，计算时**释放 GIL**。所以线程也能并行：
```python
def chunk(lo, hi):
    x = np.arange(lo, hi, dtype=np.float64)
    return float((np.sqrt(x) * np.sin(x)).sum())
with ThreadPoolExecutor(8) as ex:
    p = sum(ex.map(chunk, range(0, N, N//8), range(N//8, N+1, N//8)))
```
实测（1 亿个元素，一次测量）：NumPy 单线程 1.71 秒，8 个线程 1.04 秒，约 1.6 倍。受限于内存带宽：数组运算每个元素的计算量小，瓶颈在读写内存。

**2. 多进程**：`multiprocessing.Pool` / `concurrent.futures.ProcessPoolExecutor` 启动多个子进程，每个有自己的 GIL，真正并行。数据通过序列化（pickle）传给子进程，所以要传大块、结果要小。
```python
with Pool(4) as p:
    total = sum(p.starmap(count, [(k*N//4, (k+1)*N//4) for k in range(4)]))
```
适合“纯 Python 的 CPU 密集函数，每个任务够大”。

**3. 其他**：Numba（把 Python 函数即时编译成机器码并可并行）、Cython、Polars/DataFusion 这类多线程的列式引擎、Dask/Ray（分布式）。

**选择**：能表达成数组运算 → NumPy/Polars；是大块纯 Python 逻辑 → 多进程；任务小而多 → 批量化后再并行，否则序列化开销吃掉收益。
