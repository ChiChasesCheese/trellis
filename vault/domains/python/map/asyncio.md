%% trellis:begin %%
# asyncio 异步编程

单线程事件循环上的协作式多任务：协程、任务与 Future 的关系，`await` 让出控制权的机制，取消与超时，以及与线程和阻塞代码的交界。

## Topics
- [[domains/python/map/asyncio.event-loop|事件循环：单线程协作式多任务如何工作]]
- [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]
- [[domains/python/map/asyncio.futures|Future：可等待的占位符与回调]]
- [[domains/python/map/asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]]
- [[domains/python/map/asyncio.cancellation|取消：`CancelledError`、清理与不可取消的边界]]
- [[domains/python/map/asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]]
- [[domains/python/map/asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]]
- [[domains/python/map/asyncio.debugging|常见 bug 与调试：漏 `await`、循环已在运行、异常被吞、`PYTHONASYNCIODEBUG`]]
- [[domains/python/map/asyncio.streams-protocols|网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法]]
- [[domains/python/map/asyncio.contextvars|上下文变量（contextvars）：为什么线程局部存储在 `await` 之间会失效]]
%% trellis:end %%

## Notes
