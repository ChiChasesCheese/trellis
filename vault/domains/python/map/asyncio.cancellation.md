%% trellis:begin %%
# 取消：`CancelledError`、清理与不可取消的边界
*asyncio 异步编程*

理解 `task.cancel()` 在下一次 await 处注入 `CancelledError`、`finally` 中的清理、`asyncio.shield` 保护关键段，以及取消被吞掉的常见 bug。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]]

## Readings
- [[fowler-02-asyncio-basics|Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试]]
- [[pydocs-asyncio-coroutines-tasks|asyncio：协程与任务完整参考]]

## Drills
- [[asyncio-fix-the-silent-async-script|Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug]]

## Cards (6)
1. [[cancel-return-false-if-already-done]]
2. [[cancellederror-subclasses-baseexception]]
3. [[finally-cleanup-runs-on-cancellation]]
4. [[shield-protects-inner-task-not-outer-await]]
5. [[suppress-cancelled-error-requires-uncancel]]
6. [[task-cancel-injects-at-next-await]]
%% trellis:end %%

## Notes
