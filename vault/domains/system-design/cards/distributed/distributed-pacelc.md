---
id: distributed-pacelc
node: distributed.cap
type: qa
---
## Q
What does PACELC add over CAP, and how do DynamoDB and Spanner classify under it?

## A
The **ELC part**: *Else* (no partition, i.e. almost always), you still trade **Latency vs Consistency** — strong consistency requires coordination (quorum/leader round-trips) on every operation, paying latency even on a healthy network.

- **DynamoDB (default), Cassandra: PA/EL** — on partition choose availability; normally choose low latency (eventual consistency).
- **Spanner, CockroachDB, ZooKeeper: PC/EC** — on partition refuse minority-side operations; normally pay coordination latency for strong consistency.

Interview use: PACELC explains why "strongly consistent" systems are slower *every day*, not just during rare partitions.

## Q zh
PACELC 比 CAP 多说了什么？DynamoDB 和 Spanner 在这个框架下分别怎么分类？

## A zh
多出来的是 **ELC 部分**：*Else*（没有分区的时候，也就是绝大多数时候），你仍然要在**延迟（Latency）和一致性（Consistency）**之间权衡——强一致性需要在每次操作上都进行协调（quorum/leader 往返），即使网络健康也要付出延迟。

- **DynamoDB（默认）、Cassandra：PA/EL** —— 分区时选可用性；平时选低延迟（最终一致）。
- **Spanner、CockroachDB、ZooKeeper：PC/EC** —— 分区时拒绝少数派一侧的操作；平时为强一致性付出协调延迟。

面试用法：PACELC 解释了为什么"强一致"的系统*每天*都更慢，而不只是在罕见的分区期间。
