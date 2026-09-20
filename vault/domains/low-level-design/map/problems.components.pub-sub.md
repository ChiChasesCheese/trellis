%% trellis:begin %%
# 发布订阅与事件总线（Pub-Sub）
*设计题（Design Problems） / 基础组件*

主题、订阅者、消息分发与位点，线程安全的进程内消息队列。

**Requires:** [[domains/low-level-design/map/patterns.observer|观察者与事件（Observer）]], [[domains/low-level-design/map/concurrency.patterns|并发模式]]

## Readings
- [[solution-pub-sub|设计题解：发布订阅与事件总线（Pub-Sub）]]
- [[src-ashishps1-pub-sub|awesome-low-level-design — Designing a Pub-Sub System]]
- [[src-interviewready-pub-sub|InterviewReady/Low-Level-Design — distributed-event-bus]]
- [[src-pyqueue-pub-sub|queue — A synchronized queue class（标准库文档）]]

## Drills
- [[design-pub-sub|Drill：发布订阅与事件总线（Pub-Sub）]]

## Cards (10)
1. [[problems-pub-sub-push-vs-pull]]
2. [[problems-pub-sub-cursor-owned-by-topic]]
3. [[problems-pub-sub-shared-log-vs-per-subscriber-queue]]
4. [[problems-pub-sub-overflow-policy-three]]
5. [[problems-pub-sub-eviction-condition]]
6. [[problems-pub-sub-ordering-guarantee-scope]]
7. [[problems-pub-sub-failing-subscriber-isolation]]
8. [[problems-pub-sub-unsubscribe-releases-cursor]]
9. [[problems-pub-sub-dead-letter-is-a-topic]]
10. [[problems-pub-sub-no-new-singleton]]
%% trellis:end %%

## Notes
