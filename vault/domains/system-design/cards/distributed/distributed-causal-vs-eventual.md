---
id: distributed-causal-vs-eventual
node: distributed.consistency
type: qa
---
## Q
Under plain eventual consistency, a user sees the reply "No it isn't" before the question it answers. What guarantee prevents this, and what does it deliberately not order?

## A
**Causal consistency**: if write B was made after seeing write A (same session, or read-then-write), every node must apply/expose A before B. Implemented with version vectors or by tracking each write's causal dependencies and delaying delivery until they're satisfied.

It deliberately does **not** order concurrent writes — updates with no causal path between them may be seen in different orders by different nodes. That's why it's cheaper than linearizability: it's the strongest model that stays available during partitions.

## Q zh
在普通的最终一致性下，用户会在看到问题之前先看到回复 "不是这样的"。什么保证能防止这种情况？它又刻意不保证什么顺序？

## A zh
**因果一致性**：如果写 B 是在看到写 A 之后发生的（同一会话，或者先读后写），那么每个节点在应用/展示 B 之前都必须先应用/展示 A。实现方式是使用 version vector，或者跟踪每次写入的因果依赖，直到这些依赖被满足才投递。

它刻意**不**为并发写排序：没有因果路径相连的更新，不同节点可能看到不同的顺序。这正是它比线性一致性便宜的原因：它是在分区期间仍能保持可用的最强模型。
