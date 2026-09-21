---
id: call-soon-threadsafe-for-touching-asyncio-from-other-thread
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
在另一个 OS 线程里直接调用 `fut.cancel()` 去操作一个属于事件循环的 Future 对象，安全吗？正确做法是什么？

## A
不安全：几乎所有 asyncio 对象都不是线程安全的，跨线程直接调用它们的方法可能和事件循环所在线程产生数据竞争。正确做法是用 `loop.call_soon_threadsafe(fut.cancel)`，把这次调用作为一个回调安全地排进事件循环的调度队列，由事件循环所在线程自己去执行。
