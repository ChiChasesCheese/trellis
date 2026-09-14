---
id: storage-online-migration-vs-one-shot
node: storage.relational.operations
type: qa
---
## Q
You must move hundreds of millions of live rows to a new data model. Why is a one-shot migration (a single `ALTER TABLE`, or one big copy script run overnight) the wrong tool, and what does the incremental dual-write approach buy instead?

## A
One-shot fails on three counts:
- **Locking / load**: a table rewrite or bulk copy hammers the primary and can block writes for hours on a table that must keep serving production traffic.
- **Unrateable risk**: it is all-or-nothing — you cannot pause it, slow it down, or find out halfway that 0.1% of rows convert wrongly without partial, inconsistent state.
- **No rollback**: once the old shape is destroyed (or writes have moved), there is no cheap way back.

Incremental (dual-write → backfill → verify → cut over) buys the opposites: the backfill is **rate-limited and checkpointed** (resumable, tunable against production load), a **verification gate** compares old vs new before any traffic depends on the new store, and **every phase is reversible** — the old path stays authoritative until the new one is proven, so aborting at any point loses nothing.

## Q zh
你要把数亿行线上数据迁到新的数据模型。为什么一次性迁移（一条 `ALTER TABLE`，或一个通宵跑完的大拷贝脚本）是错误的工具？增量式 dual-write 方案换来了什么？

## A zh
一次性迁移在三点上失败：
- **锁 / 负载**：表重写或批量拷贝会重压主库，可能让一张必须持续服务生产流量的表阻塞写入数小时。
- **风险无法调节**：全有或全无 — 你不能暂停、不能减速，也无法在中途发现 0.1% 的行转换错误而不留下部分迁移的不一致状态。
- **无法回滚**：一旦旧数据形态被销毁（或写入已切走），就没有廉价的退路。

增量式（dual-write → backfill → verify → 切换）换来的正是反面：backfill **限速且带 checkpoint**（可恢复、可根据生产负载调节），**验证关卡**在任何流量依赖新存储之前比对新旧数据，且**每个阶段都可回退** — 在新路径被证明正确之前旧路径始终是权威，任何时刻中止都不损失什么。
