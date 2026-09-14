---
id: storage-mvcc-vacuum
node: storage.relational.operations
type: qa
---
## Q
Postgres MVCC: what physically happens on `UPDATE`, and what operational problem does that create at high churn?

## A
Nothing is overwritten: `UPDATE` writes a **new row version** and marks the old one with the updating transaction's ID; each snapshot sees the versions visible to it. That's how readers never block writers.

Problem: dead versions accumulate as **bloat** — tables and indexes grow, scans wade through dead tuples, and **vacuum** must reclaim them. At high update churn, vacuum falling behind means degrading performance and, in the extreme, transaction-ID wraparound forcing an emergency shutdown.

Interview-grade mitigations: tune autovacuum aggressively on hot tables, keep long-running transactions off the primary (they pin old versions), and prefer HOT updates (don't index the churning column).

## Q zh
Postgres MVCC：`UPDATE` 物理上发生了什么，那在高流失率下创建了什么运维问题？

## A zh
没有什么被覆盖：`UPDATE` 写一个**新行版本**并用更新事务 ID 标记旧版本；每个快照看到对它可见的版本。这就是读端永远不阻塞写端的原因。

问题：死版本作为**膨胀**累积——表和索引增长，扫描涉水通过死元组，**vacuum** 必须回收它们。在高更新流失率，vacuum 落后意味着性能降级，极端情况强制事务 ID 换行迫使紧急关闭。

面试级别缓解：在热表上激进地调整 autovacuum，从主库中保持长运行事务（它们 pin 旧版本），并偏好 HOT 更新（不索引流失列）。
