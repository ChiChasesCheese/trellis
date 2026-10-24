---
id: pl-conc-concepts-unique-python
node: concurrency.concepts
type: qa
step: 6
---
## Q
同样的「数素数」CPU 密集任务，Python 用 4 个 `threading.Thread` 分区间计算，会比单线程快吗？这和 Java、Rust 的行为差在哪里？

## A
不会。代码：
```python
N = 400_000
t = time.perf_counter(); count(0, N)
print(f"1 thread  {time.perf_counter()-t:.2f}s")
t = time.perf_counter()
ts = [Thread(target=count, args=(k*N//4, (k+1)*N//4)) for k in range(4)]
[x.start() for x in ts]; [x.join() for x in ts]
print(f"4 threads {time.perf_counter()-t:.2f}s")
```
输出（Python 3.14 默认构建）：`1 thread 0.32s`、`4 threads 0.32s`。4 个线程的总时间与单线程相同。

原因：默认的 CPython 有全局解释器锁（GIL），同一时刻只有持有它的线程能执行 Python 字节码。4 个线程只是轮流拿锁，CPU 密集代码里没有阻塞调用去释放它，所以没有并行，还多了切换开销。Java 与 Rust 的线程没有这把锁，4 个线程真的在 4 个核上同时算，同类任务约快 2.7 倍。

结论：Python 里线程是并发工具而不是并行工具。要用多核算 CPU 密集任务，改用 `multiprocessing`（每个进程一个解释器、一把 GIL），或把热点放进释放 GIL 的 C 扩展（NumPy 等）。
