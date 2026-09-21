---
id: threads-when-suited
node: concurrency.threads
type: qa
source: python-docs
---
## Q
`threading` 模块适合什么样的任务，为什么？

## A
适合 I/O 密集（I/O-bound）任务，例如文件读写、网络请求：线程发起阻塞调用时会释放 GIL，等待期间其他线程可以继续工作，多个线程能把等待时间重叠起来，从而缩短总耗时。对 CPU 密集任务，同一进程内所有线程仍共享同一把 GIL，无法并行执行字节码，应改用 `multiprocessing` 或 `ProcessPoolExecutor`。
