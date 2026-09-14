---
id: distributed-leaderless-staleness-monitoring
node: distributed.replication.leaderless
type: qa
---
## Q
For a leader-based database you graph replication lag on a dashboard. Why can't you build the same "how stale are reads" graph for a leaderless store, and what do you do instead?

## A
- **Leader-based lag is measurable by subtraction**: writes are applied in one order from a single log, so `leader position − follower position` (or the timestamp of the last applied entry) is a meaningful, exact lag.
- **Leaderless stores have no such position**: writes arrive at replicas in different orders, there is no shared log offset to compare, and with read repair only (no anti-entropy) a rarely-read key's replicas can stay divergent for an *unbounded* time. "Eventual" comes with no measurable bound.
- What you do instead:
  - Rely on **quorum math** (N, W, R) for the expected-case guarantee, and monitor its *inputs*: node availability, hinted-handoff backlog, dropped writes.
  - Track **repair health**: anti-entropy runs completing on schedule, sibling/conflict rates.
  - If you need a number, **measure empirically**: write canary keys and time how long until all replicas agree.

## Q zh
对于基于 leader 的数据库，你可以在仪表盘上画出 replication lag（复制滞后）曲线。为什么在无主（leaderless）存储上画不出同样的"读有多陈旧"的图？替代做法是什么？

## A zh
- **leader 型的 lag 可以用减法量出来**：写入按单一日志的同一顺序应用，所以 `leader 位点 − follower 位点`（或最后应用条目的时间戳）是一个有意义、精确的滞后值。
- **无主存储没有这样的位点**：写入以不同顺序到达各副本，没有可比较的共享日志 offset；如果只有 read repair、没有 anti-entropy（反熵修复），一个很少被读的 key 的各副本可以在*无界*的时间里保持分歧。"最终一致"不附带任何可测量的上界。
- 替代做法：
  - 依靠 **quorum 数学**（N、W、R）提供常态下的保证，并监控它的*输入*：节点可用性、hinted handoff 积压、被丢弃的写。
  - 跟踪**修复健康度**：anti-entropy 是否按计划完成、sibling/冲突率。
  - 如果必须要一个数字，就**实证测量**：写入金丝雀（canary）key，计时多久之后所有副本达成一致。
