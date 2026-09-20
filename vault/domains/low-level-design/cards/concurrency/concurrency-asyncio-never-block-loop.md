---
id: concurrency-asyncio-never-block-loop
node: concurrency.asyncio
type: qa
step: 4
---
## Q
在一个 `async def` 函数里直接调用一个耗时的同步（阻塞）函数，比如 `time.sleep(2)` 或一次同步的数据库查询，会有什么后果？

## A
因为整个 `asyncio` 只有一个线程在跑，这次阻塞调用会占住事件循环所在的唯一线程，直到它返回为止——事件循环没有机会去调度任何其他协程，哪怕它们早就就绪了。结果是所有并发任务的延迟都被这一次调用拖累，`asyncio` 承诺的"大量并发"直接失效。

正确做法是把阻塞调用丢给一个线程池去跑，让事件循环继续调度别的协程：

```python
async def handler():
    result = await asyncio.to_thread(blocking_db_call, query)
    # 等价于 await loop.run_in_executor(None, blocking_db_call, query)
```

`asyncio.to_thread`（`run_in_executor(None, ...)` 的简化封装）适合阻塞式 I/O；如果是真正的 CPU 密集计算，丢进线程池一样抢不过 GIL，需要 `run_in_executor` 配合 `ProcessPoolExecutor`。
