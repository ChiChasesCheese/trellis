---
nodes: [amazon.amz-emergency-pubsub, patterns.observer]
tags: [problem]
---
# Drill：应急事件发布订阅（Emergency Pub/Sub）

一个应急响应系统里，一些组件订阅应急事件，另一些组件发布事件，请实现处理发布与订阅逻辑的类。规模是一个进程内的组件，几十个订阅者，几个发布线程。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`subscribe(handler)`、`unsubscribe`、`publish(topic, severity, message)`，事件是冻结的数据对象并带一个递增编号，同步送给所有订阅者。想清楚：处理函数是谁的责任，事件里该带什么。
- 第 2 关（约 15 分钟）：订阅者可以只订某些事件类型、只收不低于某个严重度的事件；**一个订阅者抛异常，其他订阅者必须照常收到**，出错的订阅者可以重试几次，仍失败就记到死信列表。想清楚：这条保证放在哪一层，`KeyboardInterrupt` 要不要也吞掉。
- 第 3 关（约 15 分钟）：处理函数在 `publish` 里再发布、再退订自己，不能死锁；慢订阅者不能拖住发布者和其他订阅者。想清楚：锁在哪里放开，为什么调用订阅者代码时不能持锁。
- 第 4 关（选做）：异步订阅者：每人一个有界信箱，严重度高的先出，满了挤掉最不重要且最旧的一条；`flush` 与 `close`。判分点：第 1 到 3 关的类一行不改。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-emergency-pubsub/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-emergency-pubsub -q`。

**评分点**
- 开场问清同步还是异步、失败怎么办、要不要过滤与优先级（[[amz-emergency-pubsub-prompt-and-three-questions]]）。
- 总线、订阅者、信箱各管一件事，说得出划分依据（[[amz-emergency-pubsub-objects-and-one-job-each]]）。
- `publish` 持锁只拍快照，处理函数在锁外调用（[[amz-emergency-pubsub-stage1-publish-flow-code]]、[[amz-emergency-pubsub-holding-lock-while-calling-handlers]]）。
- 失败隔离的边界放在 `Subscription.deliver` 一处（[[amz-emergency-pubsub-failure-boundary-in-subscription]]）。
- 过滤只加一个判断，总线不改（[[amz-emergency-pubsub-followup-topic-and-severity-filter]]）。
- 重试用完进死信，且死信有上限（[[amz-emergency-pubsub-retry-then-dead-letter]]）。
- 慢订阅者各自一个信箱，满了挤掉最不重要的（[[amz-emergency-pubsub-slow-subscriber-mailbox]]、[[amz-emergency-pubsub-priority-heap-order]]）。

**题解**：[[solution-amz-emergency-pubsub]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
