---
id: concurrency-cpu-vs-io-bound-choice
node: concurrency.model
type: qa
step: 5
---
## Q
同样是"并发处理一批任务"，什么时候该用线程（threading）、什么时候该用进程（multiprocessing）、什么时候该用协程（asyncio）？

## A
先分清任务是 CPU 密集（计算多、几乎不等待）还是 I/O 密集（大部分时间在等网络、磁盘、数据库）。GIL 只在执行 Python 字节码时持有，线程做 I/O 等待（网络调用、`time.sleep`、文件读写）时会释放 GIL，所以**I/O 密集**任务用 `threading`（或 `asyncio`）能真正并发；但**CPU 密集**的纯 Python 计算，多个线程会互相抢 GIL、几乎不提速，需要 `multiprocessing` 用多个解释器进程绕开 GIL。

`asyncio` 是单线程的协作式调度，适合大量并发的 I/O 等待（比如上万个网络连接），比线程更省内存、没有锁竞争，但要求整条调用链都是 `async`；如果只是少量线程、且要调用不支持 `async` 的阻塞库，线程更简单。
