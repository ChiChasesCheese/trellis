---
id: distributed-internal-vs-heterogeneous-2pc
node: distributed.transactions.distributed
type: qa
---
## Q
Spanner and CockroachDB run two-phase commit on essentially every cross-shard write and perform fine, while XA-style 2PC across a database plus a message broker is notorious. Same protocol — what makes the internal case workable and the heterogeneous case not?

## A
- **The participants are replicated shards, not single machines.** In an internal system each participant and the coordinator state live in a Paxos/Raft group — a "participant failure" is a sub-second leader failover, not an in-doubt transaction awaiting recovery. XA's participants and its app-server coordinator are single points whose crash leaves locks held indefinitely.
- **One team owns the whole protocol**, so it can be co-designed and optimized: transaction-aware timestamps, pipelined/parallel commits, batching prepares with reads. XA is a lowest-common-denominator C-era interface bolted onto systems that barely maintain it; nothing can be optimized end to end.
- **Failure semantics are uniform.** Internally, every participant recovers the same way from the same kind of log. Heterogeneous participants (a DB, a broker) have different durability models and recovery tooling, so resolution of stuck transactions falls to humans.

Rule of thumb: distributed transactions *within* one strongly-consistent system are an implementation detail; distributed transactions *across* independently-operated systems are an architecture smell — use outbox/sagas there.

## Q zh
Spanner 和 CockroachDB 几乎在每一次跨 shard 写入上都运行两阶段提交（2PC），表现良好；而跨"数据库 + 消息 broker"的 XA 式 2PC 却臭名昭著。协议相同——为什么内部场景可行、异构场景不行？

## A zh
- **参与者是有副本的 shard，不是单台机器。** 在内部系统里，每个参与者和协调者的状态都放在 Paxos/Raft 组中——"参与者故障"是一次亚秒级的 leader 切换，而不是一笔等待人工恢复的 in-doubt 事务。XA 的参与者和它的应用服务器协调者都是单点，一旦崩溃锁就被无限期占住。
- **整套协议由一个团队掌控**，因此可以协同设计和优化：感知事务的时间戳、流水线/并行提交、把 prepare 和读操作合并批处理。XA 则是一个"最小公分母"的 C 时代接口，被拧在一批勉强维护它的系统上；端到端什么都优化不了。
- **故障语义是统一的。** 内部系统里每个参与者都以同样的方式、从同一种日志中恢复。异构参与者（一个数据库、一个 broker）的持久化模型和恢复工具各不相同，卡住的事务只能靠人来收拾。

经验法则：*同一个*强一致系统内部的分布式事务是实现细节；*跨*独立运维系统的分布式事务是架构异味——那里请用 outbox/saga。
