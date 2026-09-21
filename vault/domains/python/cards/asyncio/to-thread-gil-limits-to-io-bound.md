---
id: to-thread-gil-limits-to-io-bound
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
能不能用 `asyncio.to_thread()` 来给 CPU 密集型计算提速？

## A
一般不能。由于全局解释器锁（GIL）的存在，多个线程之间的 CPU 密集代码仍然互相抢占同一个解释器锁，无法真正并行，`asyncio.to_thread()` 因此主要适用于 I/O 密集型阻塞调用；只有在自由线程（free-threaded）构建的 Python（没有 GIL）下，它才能用于 CPU 密集函数。
