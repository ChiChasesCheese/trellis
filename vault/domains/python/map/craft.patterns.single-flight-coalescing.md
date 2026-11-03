%% trellis:begin %%
# 单飞/请求合并：同一件事只做一次，后到者等结果
*编码功力（Coding Craft） / 跨题模式（Patterns）*

热点 key 同时未命中时只回源一次；重复请求并入第一个请求；占了坑但没结果时返回「进行中」。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]

## Cards (5)
1. [[craft-single-flight-coalescing-1-cache-stampede]]
2. [[craft-single-flight-coalescing-2-order-and-handoff]]
3. [[craft-single-flight-coalescing-3-coalesce-duplicate-requests]]
4. [[craft-single-flight-coalescing-4-wait-or-report-in-flight]]
5. [[craft-single-flight-coalescing-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
