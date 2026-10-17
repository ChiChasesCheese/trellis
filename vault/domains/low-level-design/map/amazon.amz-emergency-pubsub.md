%% trellis:begin %%
# 应急事件发布订阅（Emergency Pub/Sub）
*Amazon 专项（Amazon OOD）*

组件订阅 / 发布应急事件；一个订阅者失败不拖累其他人，主题过滤、优先级与重试。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.observer|观察者与事件（Observer）]]

## Readings
- [[solution-amz-emergency-pubsub|设计题解：应急事件发布订阅（Emergency Pub/Sub）]]
- [[src-hellointerview-amz-emergency-pubsub|Hello Interview 社区题库：Amazon（题目 publish-subscribe-system）]]
- [[src-pythondocs-amz-emergency-pubsub|heapq — Heap queue algorithm（Python 标准库文档）]]

## Drills
- [[design-amz-emergency-pubsub|Drill：应急事件发布订阅（Emergency Pub/Sub）]]

## Cards (9)
1. [[amz-emergency-pubsub-prompt-and-three-questions]]
2. [[amz-emergency-pubsub-objects-and-one-job-each]]
3. [[amz-emergency-pubsub-stage1-publish-flow-code]]
4. [[amz-emergency-pubsub-priority-heap-order]]
5. [[amz-emergency-pubsub-failure-boundary-in-subscription]]
6. [[amz-emergency-pubsub-followup-topic-and-severity-filter]]
7. [[amz-emergency-pubsub-retry-then-dead-letter]]
8. [[amz-emergency-pubsub-slow-subscriber-mailbox]]
9. [[amz-emergency-pubsub-holding-lock-while-calling-handlers]]
%% trellis:end %%

## Notes
