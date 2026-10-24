---
id: pl-conc-gil-pitfall-multiprocessing
node: concurrency.gil
type: qa
step: 10
---
## Q
用 `multiprocessing` 绕开 GIL 时，为什么有时候比单进程还慢？序列化开销有多大？

## A
进程之间不共享内存。参数和返回值要经过序列化（pickle）、通过管道传给另一个进程、再反序列化；每个子进程还要启动一个解释器并导入模块。当任务本身很小，这些固定开销就压过了并行的收益。

实测（Python 3.14，一次测量）：对一个含 500 万个整数的列表求和：
```python
xs = list(range(5_000_000))
total(xs)                     # in-process: 0.008 s
pool.apply(total, (xs,))      # via 1 worker process: 0.113 s
```
进程内直接算 0.008 秒；交给一个已启动的工作进程算 0.113 秒，慢了约 14 倍。仅把这个列表 pickle 就要约 25 MB、0.03 秒，其余是管道传输和对端反序列化。计算本身（0.008 秒）远小于搬运数据的成本。

规律：多进程的收益需要 **计算量 ≫ 数据搬运量**。

做法：
1. **粗粒度切分**：一个任务处理一大块（`chunksize`），而不是每个元素一个任务。
2. **少传数据**：让子进程自己读文件、传文件名而不是内容；大数组用 `multiprocessing.shared_memory` 或内存映射。
3. **复用进程池**：创建一次 `Pool`，不要每次调用都新建。
4. **注意平台的启动方式**：macOS 和 Windows 默认 `spawn`（重新导入主模块，要保护 `if __name__ == "__main__"`），Linux 传统上是 `fork`（快，但与多线程混用有死锁风险，3.14 起 Linux 默认改为 `forkserver`）。
5. 返回结果也要序列化，返回大对象同样慢。
