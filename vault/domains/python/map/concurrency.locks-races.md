%% trellis:begin %%
# 竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`
*并发模型：GIL、线程与进程*

理解 `x += 1` 不是原子操作、内建容器的单个方法在 GIL 下原子但复合操作不是、死锁的四个条件与锁顺序，以及线程安全的单例/计数器实现。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]

**Unlocks:** [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]]

## Readings
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fowler-11-synchronization|Python Concurrency with asyncio · 第 11 章 同步原语]]
- [[pydocs-threading-module|threading 模块：线程、锁与同步原语]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (6)
1. [[condition-while-not-if]]
2. [[deadlock-lock-order]]
3. [[event-vs-lock-purpose]]
4. [[lock-acquire-timeout]]
5. [[lock-vs-rlock]]
6. [[semaphore-vs-bounded]]
%% trellis:end %%

## Notes
