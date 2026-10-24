---
id: pl-conc-gil-found-behavior
node: concurrency.gil
type: qa
step: 3
---
## Q
GIL（全局解释器锁）在使用时表现出什么行为？
为什么 4 个 Python 线程做 CPU 计算不会更快，而 I/O 等待的线程却可以并发？

## A
**GIL** 是 CPython 解释器里的一把全局互斥锁：任何线程要执行 Python 字节码，必须先持有它。所以**同一时刻只有一个线程在执行 Python 代码**，即使机器有 12 个核。

线程之间怎么轮换：持有 GIL 的线程运行约 5 毫秒（`sys.getswitchinterval()` 为 0.005 秒）后，如果有别的线程在等，它就在安全点放下 GIL；或者它调用阻塞操作（读写文件、`sleep`、等锁）时主动释放，返回后再抢回。

两个对照实验（一次测量，Python 3.14 默认构建）：

**CPU 密集**：数 0 到 40 万之间的素数，分成 4 个区间用 4 个线程算：
```python
ts = [Thread(target=count, args=(k*N//4, (k+1)*N//4)) for k in range(4)]
[x.start() for x in ts]; [x.join() for x in ts]
```
输出：`1 thread  0.32s`，`4 threads 0.32s`。线程轮流拿 GIL，总工作量不变，没有加速。

**I/O 等待**：8 个各 `sleep` 0.1 秒的任务，用 8 个线程：总耗时约 0.2 秒而不是顺序的 0.8 秒以上（本机 `sleep` 有定时抖动）。`sleep` 期间线程释放了 GIL，别的线程继续运行，等待重叠。

另一个有意思的现象：对 200 MB 数据做 4 次 SHA-256，顺序 0.22 秒，4 个线程 0.06 秒。`hashlib` 的 C 实现在处理大块数据时**主动释放 GIL**，所以线程真的并行了。这说明 GIL 管的是 Python 字节码的执行，不管 C 代码。

结论：Python 线程是**并发**工具（隐藏等待），不是**并行**工具（用多个核算），除非计算发生在释放 GIL 的 C 扩展里。要并行跑纯 Python 计算，需要多进程或自由线程构建。
