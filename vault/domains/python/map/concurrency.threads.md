%% trellis:begin %%
# 线程：`threading.Thread`、守护线程与线程适用的场景
*并发模型：GIL、线程与进程*

掌握用线程隐藏阻塞 I/O 的延迟、CPU 密集下多线程反而更慢的原因（GIL 争用）、守护线程的退出语义，以及线程创建的开销。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

**Unlocks:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]

## Readings
- [[cpyint-04-parallelism-concurrency|CPython Internals · 并行与并发]]
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fluent-19-concurrency-models|Fluent Python 2e · 第 19 章 Python 的并发模型]]
- [[fowler-07-blocking-work-with-threads|Python Concurrency with asyncio · 第 7 章 用线程处理阻塞任务]]
- [[pydocs-threading-module|threading 模块：线程、锁与同步原语]]

## Cards (5)
1. [[threads-creation-cost]]
2. [[threads-daemon-exit]]
3. [[threads-join-semantics]]
4. [[threads-local-vs-slots]]
5. [[threads-when-suited]]
%% trellis:end %%

## Notes
