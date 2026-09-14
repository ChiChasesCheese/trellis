---
id: analytics-time-travel-retention
node: analytics.warehouse
type: cloze
---
Lakehouse time travel works because commits never delete data files — old snapshots keep referencing them. The costs are storage growth and unbounded metadata, so tables need {{c1::snapshot expiration / vacuum}} to drop snapshots past a retention window and physically delete unreferenced files. Two operational consequences: you can only roll back or audit within {{c2::the retention window}}, and GDPR-style hard deletes aren't complete until expired snapshots' files are {{c3::physically removed}}, not just dropped from the latest snapshot.

## zh
Lakehouse 时间旅行有效因为提交从不删除数据文件 — 旧快照继续引用它们。代价是存储增长和无限元数据，所以表需要 {{c1::快照过期 / vacuum}} 删除保留窗口过去的快照并物理删除未引用的文件。两个操作后果：你只能在 {{c2::保留窗口}} 内回滚或审计，GDPR 风格的硬删除直到过期快照的文件是 {{c3::物理移除}} 才完整，不仅仅从最新快照中删除。
