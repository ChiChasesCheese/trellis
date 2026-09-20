%% trellis:begin %%
# 线程池（Thread Pool）
*设计题（Design Problems） / 基础组件*

工作线程、任务队列、Future 结果、优雅关闭与拒绝策略。

**Requires:** [[domains/low-level-design/map/concurrency.patterns|并发模式]]

## Readings
- [[solution-thread-pool|设计题解：线程池（Thread Pool）]]
- [[src-python-docs-concurrent-futures-thread-pool|concurrent.futures — Launching parallel tasks]]
- [[src-python-docs-queue-thread-pool|queue — A synchronized queue class]]

## Drills
- [[design-thread-pool|Drill：线程池（Thread Pool）]]

## Cards (8)
1. [[problems-thread-pool-base-exception-in-worker]]
2. [[problems-thread-pool-backpressure-semaphore-not-queue-maxsize]]
3. [[problems-thread-pool-admission-release-on-dequeue]]
4. [[problems-thread-pool-shutdown-wait-false-only-abandons-queued]]
5. [[problems-thread-pool-finish-atomic-check-then-act]]
6. [[problems-thread-pool-priority-queue-tie-break]]
7. [[problems-thread-pool-future-two-state]]
8. [[problems-thread-pool-cpu-vs-io]]
%% trellis:end %%

## Notes
