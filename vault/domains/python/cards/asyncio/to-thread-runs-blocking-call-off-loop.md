---
id: to-thread-runs-blocking-call-off-loop
node: asyncio.blocking-and-threads
type: qa
source: python-docs
---
## Q
协程里必须调用一个同步阻塞函数（比如 `time.sleep()` 或阻塞式文件 I/O），直接 `await asyncio.to_thread(blocking_io)` 解决了什么问题？

## A
如果在协程里直接调用 `blocking_io()`，它会占住事件循环所在的这一个线程直到执行完，期间循环上的其它任务全部卡住；`asyncio.to_thread(func, *args, **kwargs)` 把这次调用丢进一个独立线程去跑，本身立刻返回一个可以 `await` 的协程，事件循环所在线程完全不受影响，可以继续调度别的任务。
