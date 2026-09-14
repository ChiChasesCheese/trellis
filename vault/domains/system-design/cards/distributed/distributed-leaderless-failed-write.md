---
id: distributed-leaderless-failed-write
node: distributed.replication.leaderless
type: qa
---
## Q
In a Dynamo-style leaderless store (N=3, W=2), a write reaches only 1 replica and the client gets an error. Is the value gone? What must the application assume about "failed" writes?

## A
No — the value is **not rolled back**. Leaderless stores have no transaction/abort machinery: the one replica that took the write keeps it.

- Later reads may **or may not** return the "failed" value, depending on which replicas the read quorum hits.
- Worse, **read repair or anti-entropy can propagate it** to the other replicas, so the failed write can eventually *win* and become the stored value.
- Contrast with a single-leader database, where an error on commit means the transaction's effects are not visible and never will be.

Application rule: in leaderless systems an error means "**unknown outcome**, possibly durable", never "didn't happen". Safe responses are retrying with an idempotent write (same value/key, so convergence is harmless) or reading back to observe the actual state.

## Q zh
在一个 Dynamo 风格的无主（leaderless）存储中（N=3、W=2），一次写只到达了 1 个副本，客户端收到错误。这个值消失了吗？应用必须对"失败"的写做何假设？

## A zh
没有消失——这个值**不会被回滚**。无主存储没有事务/中止机制：收下这次写的那个副本会一直保留它。

- 之后的读**可能返回也可能不返回**这个"失败"的值，取决于读 quorum 命中了哪些副本。
- 更糟的是，**read repair 或 anti-entropy（反熵修复）可能把它传播**到其他副本，让这次失败的写最终*胜出*，成为存储的值。
- 对比单 leader 数据库：提交报错意味着事务的效果不可见，而且永远不会可见。

应用层规则：在无主系统里，错误的含义是"**结果未知**，甚至可能已持久化"，绝不是"没有发生"。安全的应对是用幂等写重试（同 key 同值，收敛无害），或者读回来观察实际状态。
