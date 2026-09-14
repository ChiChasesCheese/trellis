---
id: distributed-epoch-numbers
node: distributed.consensus
type: qa
---
## Q
Every consensus protocol carries an epoch number (term/ballot/view) and runs two quorum checks. What problem do epochs solve, and how do the two quorums interact?

## A
Epochs solve "**which of two would-be leaders is current**" without relying on clocks: within one epoch there is at most one leader, and a **higher epoch always defeats a lower one**.

- **Quorum 1 — election**: a candidate collects majority votes for its epoch.
- **Quorum 2 — commit**: the leader gets majority acknowledgment for each value it proposes.

The safety trick is that the two quorums **must intersect**: if a new leader was elected, every commit quorum of the old leader contains at least one node that has seen the higher epoch and therefore **rejects the old leader's proposals**. So a deposed leader can't commit anything behind the new leader's back — the generic mechanism behind Raft terms, Paxos ballots, and Viewstamped Replication views ([[distributed-raft-guarantees]] is the Raft instantiation).

## Q zh
每个共识协议都带有一个纪元号（term/ballot/view），并运行两次 quorum 检查。纪元号解决了什么问题？这两次 quorum 是怎样相互作用的？

## A zh
纪元号解决的是"两个候选 leader 中哪个才是当前的"这个问题，且不依赖时钟：在一个纪元内最多只有一个 leader，而**更高的纪元总是压过更低的**。

- **Quorum 1 —— 选举**：候选人为自己的纪元收集多数票。
- **Quorum 2 —— 提交**：leader 为它提出的每个值获得多数确认。

安全性的关键在于这两个 quorum **必须相交**：如果选出了新 leader，那么旧 leader 的每一个提交 quorum 里都至少有一个节点已经见过更高的纪元，因此会**拒绝旧 leader 的提议**。所以一个被废黜的 leader 无法背着新 leader 偷偷提交任何东西——这正是 Raft 的 term、Paxos 的 ballot、Viewstamped Replication 的 view 背后的通用机制（[[distributed-raft-guarantees]] 是 Raft 的具体实现）。
