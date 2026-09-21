%% trellis:begin %%
# 选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树
*并发模型：GIL、线程与进程*

能在面试里用一句话给出结论：阻塞库 + I/O 用线程，CPU 用进程或换成 NumPy/DuckDB，高并发 I/O 且有 async 库用 asyncio，并说出每种选择的代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]

**Unlocks:** [[domains/python/map/performance.pandas-at-scale|pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制]]

## Readings
- [[fluent-19-concurrency-models|Fluent Python 2e · 第 19 章 Python 的并发模型]]
- [[fowler-01-getting-to-know-asyncio|Python Concurrency with asyncio · 第 1 章 认识 asyncio]]
- [[hpp-08-async-io|High Performance Python 2e · 第 8 章 异步 I/O]]
- [[hpp-10-clusters-job-queues|High Performance Python 2e · 第 10 章 集群与任务队列]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (5)
1. [[choosing-60s-pitch]]
2. [[choosing-cost-per-option]]
3. [[choosing-decision-tree-main]]
4. [[choosing-thread-cpu-bound-slower]]
5. [[choosing-threads-vs-asyncio-io]]
%% trellis:end %%

## Notes
