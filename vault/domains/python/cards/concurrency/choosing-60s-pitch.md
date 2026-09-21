---
id: choosing-60s-pitch
node: concurrency.choosing
type: qa
tags: [grown]
---
## Q
面试官问“Python 里线程、进程、asyncio 怎么选”，用三句话讲完，应该怎么说？

## A
第一句：先分清任务是 I/O 密集还是 CPU 密集——GIL 只挡住了 CPU 密集任务的多线程并行。第二句：I/O 密集且依赖同步库用线程，I/O 密集且追求高并发、依赖库有异步实现用 asyncio。第三句：CPU 密集用多进程绕开 GIL，或者换成释放 GIL 的 C 扩展（NumPy/DuckDB），因为进程虽然能并行但要为进程间通信和序列化的开销买单。
