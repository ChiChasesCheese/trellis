---
id: concurrency-asyncio-vs-threads-choice
node: concurrency.asyncio
type: qa
step: 6
---
## Q
在一道 LLD 题里（比如要同时处理成千上万个下游请求），什么时候应该选 `asyncio` 而不是 `threading` 线程池？

## A
当任务规模很大、且绝大部分时间花在等待 I/O（网络调用、等下游响应）而不是计算时，`asyncio` 更合适：一个线程能承载的协程数量远超能承载的操作系统线程数量（线程有 MB 级栈开销，协程只是普通对象），而且协程之间没有锁竞争和上下文切换的内核开销，写对了同步问题也更少（切换点显式在 `await`）。

但如果需要调用的库本身是同步阻塞的、没有 `async` 版本（很多传统数据库驱动、部分第三方 SDK），或者任务数量本来就不多、用线程池完全够用，硬上 `asyncio` 只是徒增"整条调用链都要 `async`"的复杂度，收益有限；这种时候直接用 `concurrent.futures.ThreadPoolExecutor` 更省事。经验法则：并发数量级到了"线程池的线程数会成为瓶颈"这个门槛,才值得为 `asyncio` 付出改写成本。
