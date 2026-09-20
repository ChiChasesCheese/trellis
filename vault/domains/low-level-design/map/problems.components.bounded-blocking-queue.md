%% trellis:begin %%
# 有界阻塞队列（Bounded Blocking Queue）
*设计题（Design Problems） / 基础组件*

用 Condition 实现的生产者-消费者：满则阻塞、空则等待、超时与关闭。

**Requires:** [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]]

## Readings
- [[solution-bounded-blocking-queue|设计题解：有界阻塞队列（Bounded Blocking Queue）]]
- [[src-python-docs-bounded-blocking-queue|threading — Thread-based parallelism]]
- [[src-python-docs-queue-bounded-blocking-queue|queue — A synchronized queue class]]

## Drills
- [[design-bounded-blocking-queue|Drill：有界阻塞队列（Bounded Blocking Queue）]]

## Cards (8)
1. [[problems-bounded-blocking-queue-while-not-if]]
2. [[problems-bounded-blocking-queue-two-conditions-vs-one]]
3. [[problems-bounded-blocking-queue-single-notify-lost-signal]]
4. [[problems-bounded-blocking-queue-timeout-raises]]
5. [[problems-bounded-blocking-queue-close-semantics]]
6. [[problems-bounded-blocking-queue-close-no-event]]
7. [[problems-bounded-blocking-queue-drain-reuses-wait]]
8. [[problems-bounded-blocking-queue-waiting-counts-for-tests]]
%% trellis:end %%

## Notes
