---
id: distributed-2pc-avoidance
node: distributed.transactions.distributed
type: qa
---
## Q
Why is two-phase commit avoided for cross-service transactions at scale, and what do systems do instead?

## A
2PC is a **blocking protocol with a single point of failure**: after voting "prepared", a participant must hold locks and cannot unilaterally commit or abort — if the coordinator dies, participants stay wedged (locks held, rows unavailable) until it recovers. Add: latency of two round-trips to the slowest participant, and every participant must be up (availability = product of all).

Instead: **avoid distributed transactions** — put co-mutating data in one shard/DB; or use **sagas** (local transactions + compensations) and the **outbox pattern** for atomic write-and-publish. Note: *within* one strongly-consistent database (Spanner/Cockroach), 2PC over Paxos/Raft groups is fine — the replicated coordinator removes the blocking failure mode.

## Q zh
为什么在规模化的跨服务事务中会避免两阶段提交，系统改用什么？

## A zh
2PC 是一个**阻塞型协议且有单点故障**：投票 "prepared" 后参与者必须持有锁且无法单方面提交或中止——如果协调者宕机，参与者会一直卡住（锁被占用，行不可用）直到其恢复。加上：两个往返到最慢参与者的延迟，且每个参与者都必须在线（可用性 = 所有参与者的乘积）。

替代方案：**避免分布式事务**——把互相变化的数据放在一个分片/DB；或者使用 **saga**（本地事务 + 补偿）和 **outbox pattern** 来实现原子性的写和发布。注意：*在* 一个强一致数据库（Spanner/Cockroach）内，2PC over Paxos/Raft groups 是可以的——复制的协调者消除了阻塞式故障模式。
