---
id: problems-thread-pool-cpu-vs-io
node: problems.components.thread-pool
type: qa
step: 8
tags: [grown]
---
## Q
为什么说 Python 的线程池只对 I/O 密集型任务有意义？worker 数量该怎么定？

## A
GIL（全局解释器锁）在任意时刻只允许一个线程执行 Python 字节码。I/O 密集型任务（网络调用、磁盘读写、数据库查询）在等待期间会释放 GIL，所以多个线程能真正并发地把时间花在『等』上，线程池能拿到真实的吞吐提升，worker 数量可以远超 CPU 核心数，上限取决于下游能承受多少并发连接。纯 CPU 密集的 Python 计算几乎不释放 GIL，几个 worker 线程会一直在抢同一把锁执行字节码，即使起再多线程也几乎不会更快——这种场景应该换 `multiprocessing`，用多个解释器进程绕开 GIL 而不是加更多线程。提交一个 CPU 密集型计算任务给这里设计的线程池，是这道题最容易被面试官追问、也最容易被忽视的一个误用。
