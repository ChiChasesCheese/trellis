%% trellis:begin %%
# `queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程
*并发模型：GIL、线程与进程*

掌握线程安全队列的阻塞语义、`join()`/`task_done()`、哨兵值关闭，以及"无共享状态"比加锁更可靠的设计原则。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

**Unlocks:** [[domains/python/map/craft.patterns.external-call-outside-the-lock|外部调用不持锁：占位 → 调用 → 提交（claim, call, commit）]], [[domains/python/map/craft.patterns.condition-wait-predicate-loop|条件变量：谓词 while 循环 + 精确通知（Condition wait loop）]], [[domains/python/map/craft.patterns.backpressure-overflow-policy|背压与溢出策略：丢最旧 / 阻塞 / 拒绝，必须当场选并可观测]], [[domains/python/map/craft.idioms.event-wait-and-handoff|Event / Condition 的惯用法：中断式睡眠、结果交接、截止时间]]

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
