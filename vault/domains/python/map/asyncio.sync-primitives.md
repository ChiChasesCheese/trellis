%% trellis:begin %%
# 异步同步原语与限流：`Semaphore`、`Lock`、`Queue`
*asyncio 异步编程*

掌握 `asyncio.Semaphore` 限制在途请求数、`asyncio.Queue` 做异步生产者-消费者、异步锁与线程锁的区别，以及为什么单线程仍需要锁（跨 await 的临界区）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]

**Unlocks:** [[domains/python/map/asyncio.streams-protocols|网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法]]

## Readings
- [[fowler-05-non-blocking-db-drivers|Python Concurrency with asyncio · 第 5 章 非阻塞数据库驱动]]
- [[fowler-11-synchronization|Python Concurrency with asyncio · 第 11 章 同步原语]]
- [[fowler-12-asynchronous-queues|Python Concurrency with asyncio · 第 12 章 异步队列]]
- [[pydocs-asyncio-queues|asyncio.Queue：异步生产者消费者队列]]
- [[pydocs-asyncio-sync-primitives|asyncio 同步原语：Lock / Semaphore / Event / Barrier]]

## Drills
- [[asyncio-fix-the-silent-async-script|Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug]]

## Cards (6)
1. [[asyncio-lock-acquire-is-fair]]
2. [[asyncio-lock-vs-threading-lock-key-diffs]]
3. [[condition-wait-spurious-wakeup-needs-recheck]]
4. [[queue-join-needs-task-done-per-item]]
5. [[semaphore-vs-boundedsemaphore-extra-release]]
6. [[single-thread-still-needs-lock-across-await]]
%% trellis:end %%

## Notes
