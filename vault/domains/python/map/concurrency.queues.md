%% trellis:begin %%
# `queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程
*并发模型：GIL、线程与进程*

掌握线程安全队列的阻塞语义、`join()`/`task_done()`、哨兵值关闭，以及"无共享状态"比加锁更可靠的设计原则。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Readings
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fowler-12-asynchronous-queues|Python Concurrency with asyncio · 第 12 章 异步队列]]
- [[pydocs-queue-module|queue 模块：线程安全队列]]

## Cards (5)
1. [[queue-daemon-sentinel]]
2. [[queue-fifo-lifo-priority]]
3. [[queue-join-taskdone]]
4. [[queue-no-shared-state]]
5. [[queue-qsize-not-reliable]]
%% trellis:end %%

## Notes
