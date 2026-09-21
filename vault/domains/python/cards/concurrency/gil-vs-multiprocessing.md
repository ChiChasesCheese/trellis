---
id: gil-vs-multiprocessing
node: concurrency.gil
type: qa
source: python-docs
---
## Q
为什么说多线程（threading）在 CPU 密集型任务上无法利用多核，而多进程（multiprocessing）可以？

## A
同一进程内的所有线程共享同一把 GIL，任意时刻只有一个线程在执行 Python 字节码，所以多线程跑纯 Python 计算不会有并行加速，甚至因为线程切换和 GIL 争用（contention）而变慢。多进程启动的是独立的操作系统进程，每个进程有自己的解释器和 GIL，因此能真正在多个 CPU 核心上并行执行，代价是进程间通信需要经过 pickle 序列化。
