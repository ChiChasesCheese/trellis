%% trellis:begin %%
# 并发模式
*并发（Concurrency）*

生产者-消费者、有界阻塞队列、线程池与 `concurrent.futures`、读写锁、安全的惰性初始化。

**Requires:** [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]]

**Unlocks:** [[domains/low-level-design/map/problems.components.pub-sub|发布订阅与事件总线（Pub-Sub）]], [[domains/low-level-design/map/problems.components.task-scheduler|任务调度器（Task Scheduler）]], [[domains/low-level-design/map/problems.components.thread-pool|线程池（Thread Pool）]]

## Readings
- [[java-concurrency-in-practice|Java Concurrency in Practice (Goetz et al.)]]
- [[ostep-semaphores|Semaphores (OSTEP, Arpaci-Dusseau — free chapter)]]

## Drills
- [[design-pub-sub|Drill：发布订阅与事件总线（Pub-Sub）]]
- [[design-task-scheduler|Drill：任务调度器（Task Scheduler）]]
- [[design-thread-pool|Drill：线程池（Thread Pool）]]

## Cards (7)
1. [[concurrency-producer-consumer-queue]]
2. [[concurrency-bounded-queue-invariants]]
3. [[concurrency-threadpool-future]]
4. [[concurrency-thread-pool-backpressure]]
5. [[concurrency-rwlock-when]]
6. [[concurrency-double-checked-locking]]
7. [[concurrency-single-condvar-lost-signal]]
%% trellis:end %%

## Notes
