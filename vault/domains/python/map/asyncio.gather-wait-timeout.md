%% trellis:begin %%
# 并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`
*asyncio 异步编程*

掌握 `gather` 保序返回且默认第一个异常传播、`return_exceptions=True` 收集异常、`wait_for` 超时会取消任务，以及 3.11 `TaskGroup` 的结构化并发与异常组。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]]

**Unlocks:** [[domains/python/map/asyncio.cancellation|取消：`CancelledError`、清理与不可取消的边界]], [[domains/python/map/asyncio.debugging|常见 bug 与调试：漏 `await`、循环已在运行、异常被吞、`PYTHONASYNCIODEBUG`]]

## Readings
- [[fluent-21-async-programming|Fluent Python 2e · 第 21 章 异步编程]]
- [[fowler-04-concurrent-web-requests|Python Concurrency with asyncio · 第 4 章 并发网络请求：gather、as_completed、超时]]
- [[pydocs-asyncio-coroutines-tasks|asyncio：协程与任务完整参考]]

## Drills
- [[asyncio-fix-the-silent-async-script|Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug]]

## Cards (6)
1. [[gather-default-first-exception-propagates]]
2. [[gather-return-exceptions-true-aggregates]]
3. [[gather-schedules-coroutines-as-tasks]]
4. [[taskgroup-cancels-siblings-on-error-gather-does-not]]
5. [[taskgroup-exception-group-multiple-failures]]
6. [[wait-for-timeout-cancels-and-waits]]
%% trellis:end %%

## Notes
