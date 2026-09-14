---
id: storage-replica-lag-ops
node: storage.relational.operations
type: qa
---
## Q
You run Postgres read replicas. How do you actually measure replication lag (two units matter), and what workload events typically make it spike even when the network is fine?

## A
Measure both:

- **Bytes**: how far the replica's applied WAL position (LSN) trails the primary's — the true backlog size, meaningful even when writes are bursty.
- **Seconds**: how old the last replayed record is — what users experience as staleness. Caveat: on an idle primary "seconds" can look huge with zero real backlog, so alert on the pair.

Typical spike causes:

- **Write bursts on the primary** — bulk loads, big migrations, mass deletes generate WAL faster than one replica replay process can apply it.
- **Replay vs query conflict on the replica**: replaying a vacuum cleanup would invalidate rows a long-running replica query still needs — the replica either pauses replay (lag climbs) or cancels the query. `hot_standby_feedback` avoids cancellations by making the primary retain old versions, trading replica lag for primary bloat.

Why it's worth an alert: lag is simultaneously your stale-read window and — if the primary dies — your data-loss exposure on failover.

## Q zh
你在运营 Postgres 读副本。如何实际度量复制延迟（replication lag，两个单位都重要），以及在网络正常时哪些工作负载事件通常会让它飙升？

## A zh
两个都要量：

- **字节**：副本已应用的 WAL 位置（LSN）落后主库多少 — 真正的积压大小，即使写入是突发的也有意义。
- **秒**：最后一条已重放记录有多旧 — 用户体感的陈旧程度。注意：主库空闲时"秒数"可能看起来巨大而实际积压为零，所以要成对告警。

典型的飙升原因：

- **主库写入突发** — 批量导入、大迁移、批量删除产生 WAL 的速度超过副本单个重放进程的应用速度。
- **副本上重放与查询的冲突**：重放一次 vacuum 清理会使副本上长查询仍需要的行失效 — 副本要么暂停重放（lag 上升），要么取消查询。`hot_standby_feedback` 通过让主库保留旧版本来避免取消查询，代价是用主库膨胀（bloat）换副本延迟。

为什么值得告警：lag 同时是你的陈旧读窗口，以及 — 主库挂掉时 — failover 的数据丢失敞口。
