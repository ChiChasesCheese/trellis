%% trellis:begin %%
# 多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存
*并发模型：GIL、线程与进程*

理解进程绕过 GIL 实现真并行、参数与返回值必须可 pickle、fork 在多线程程序中的危险与 3.14 起 POSIX 默认 forkserver（Windows/macOS 仍是 spawn）、`shared_memory` 与 `Manager` 的取舍。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

**Unlocks:** [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]

## Readings
- [[cpyint-04-parallelism-concurrency|CPython Internals · 并行与并发]]
- [[fluent-19-concurrency-models|Fluent Python 2e · 第 19 章 Python 的并发模型]]
- [[fowler-06-cpu-bound-work|Python Concurrency with asyncio · 第 6 章 处理 CPU 密集型任务：配合进程池]]
- [[hpp-09-multiprocessing|High Performance Python 2e · 第 9 章 multiprocessing 模块]]
- [[pydocs-multiprocessing-module|multiprocessing 模块：绕开 GIL 的真并行]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (6)
1. [[mp-314-default-forkserver]]
2. [[mp-bypasses-gil-needs-pickle]]
3. [[mp-lock-needed-for-output]]
4. [[mp-pool-map-vs-apply-async]]
5. [[mp-queue-vs-pipe]]
6. [[mp-start-methods-tradeoff]]
%% trellis:end %%

## Notes
