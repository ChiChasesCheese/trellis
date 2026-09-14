---
id: distributed-sync-vs-async-replication
node: distributed.replication.leader
type: qa
---
## Q
Leader-follower: synchronous vs asynchronous replication — what does each risk, and what's the standard compromise?

## A
- **Async**: leader acks before followers confirm. Risk: leader dies → **acknowledged writes are lost** on failover (the new leader never received them). Fast, and lag is unbounded under load.
- **Sync**: leader waits for follower confirmation. Zero-loss failover to that follower, but one slow/dead follower **stalls all writes**.

Compromise: **semi-synchronous** — exactly one (any one) follower must confirm, rest async; or quorum-ack (e.g. Kafka `acks=all` with `min.insync.replicas=2`). Interview framing: this is your RPO decision — async RPO > 0, sync/semi-sync RPO = 0.

## Q zh
主从复制：同步 vs 异步——各自的风险是什么？标准的折中方案是什么？

## A zh
- **异步**：leader 在 follower 确认之前就先应答。风险：leader 挂了 → 故障转移时**已确认的写会丢失**（新 leader 根本没收到它们）。速度快，负载高时延迟没有上界。
- **同步**：leader 等待 follower 确认。故障转移到那个 follower 时零丢失，但一个慢的/挂掉的 follower 会**卡住所有写入**。

折中方案：**半同步（semi-synchronous）**——恰好一个（任意一个）follower 必须确认，其余异步；或者 quorum-ack（比如 Kafka 的 `acks=all` 配合 `min.insync.replicas=2`）。面试表述：这本质上是你在做 RPO 的决策——异步 RPO > 0，同步/半同步 RPO = 0。
