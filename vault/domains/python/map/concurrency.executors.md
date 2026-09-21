%% trellis:begin %%
# `concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`
*并发模型：GIL、线程与进程*

掌握执行器的统一接口、`submit` 返回 Future、`map` 保序而 `as_completed` 先完成先出、异常在 `.result()` 时抛出，以及如何按 I/O 或 CPU 密集选执行器。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]], [[domains/python/map/concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]]

**Unlocks:** [[domains/python/map/concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]], [[domains/python/map/asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]]

## Readings
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fluent-20-concurrent-executors|Fluent Python 2e · 第 20 章 并发执行者]]
- [[hpp-09-multiprocessing|High Performance Python 2e · 第 9 章 multiprocessing 模块]]
- [[peps-pep3148-futures|PEP 3148：concurrent.futures 的执行器设计]]
- [[pydocs-concurrent-futures|concurrent.futures：线程池与进程池的统一接口]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (6)
1. [[executor-exception-on-result]]
2. [[executor-map-vs-as-completed-order]]
3. [[executor-submit-vs-map]]
4. [[processpool-cpu-vs-threadpool-io]]
5. [[threadpool-max-workers-default]]
6. [[threadpool-single-worker-deadlock]]
%% trellis:end %%

## Notes
