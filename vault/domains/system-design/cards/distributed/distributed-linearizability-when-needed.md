---
id: distributed-linearizability-when-needed
node: distributed.consistency
type: qa
---
## Q
Which concrete features genuinely require linearizability (not just causal or session guarantees), and why?

## A
Anything where **two nodes agreeing on one current value** is the point:

- **Locks and leader election**: all nodes must agree who holds the lock — a stale view means two leaders.
- **Uniqueness constraints**: usernames, one-seat-one-buyer, balance-can't-go-negative — concurrent claims must serialize on a single answer (this is a compare-and-set).
- **Cross-channel dependencies**: service A writes storage then sends a message via a queue; the consumer's read must see the write, or it processes stale data — the side channel outruns replication.

Everything else (feeds, profiles, counters) usually needs only session/causal guarantees, which don't require coordination.

## Q zh
哪些具体的功能真正需要线性一致性（而不只是因果一致或会话保证就够了）？为什么？

## A zh
任何**两个节点必须就一个当前值达成一致**才是关键的地方：

- **锁和领导者选举**：所有节点必须就谁持有锁达成一致——一个陈旧的视图就意味着两个 leader。
- **唯一性约束**：用户名、一座位一买家、余额不能为负——并发的申领必须串行化到同一个答案上（这本质上是一次 compare-and-set）。
- **跨通道依赖**：服务 A 先写存储再通过队列发一条消息；消费者读到的必须能看到那次写，否则它处理的就是陈旧数据——旁路通道跑得比复制还快。

除此之外的绝大多数场景（信息流、用户资料、计数器）通常只需要会话/因果保证，不需要协调。
