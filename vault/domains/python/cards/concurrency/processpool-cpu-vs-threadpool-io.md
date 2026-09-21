---
id: processpool-cpu-vs-threadpool-io
node: concurrency.executors
type: qa
source: python-docs
---
## Q
同样是 `Executor` 接口，什么时候该选 `ThreadPoolExecutor`，什么时候该选 `ProcessPoolExecutor`？

## A
I/O 密集型任务（网络请求、磁盘读写）选 `ThreadPoolExecutor`：线程共享内存、创建代价小，且阻塞 I/O 时会释放 GIL，多个线程能把等待时间重叠起来。CPU 密集型的纯 Python 计算选 `ProcessPoolExecutor`：每个进程有自己的 GIL，能真正利用多核并行计算；但参数和返回值必须可 pickle，且进程间没有共享内存，跨进程传大数据有序列化开销，这是它相对线程池多付出的代价。
