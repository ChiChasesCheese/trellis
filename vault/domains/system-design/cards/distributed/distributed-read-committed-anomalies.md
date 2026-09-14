---
id: distributed-read-committed-anomalies
node: distributed.transactions.isolation
type: qa
---
## Q
Give a concrete anomaly that read committed permits but repeatable read/snapshot isolation prevents, and one that *both* permit.

## A
**RC permits read skew (non-repeatable read).** Accounts A and B hold $500 each. Your report reads A ($500), a transfer of $100 A→B commits, then your report reads B ($600) — it reports $1100, money that never existed. RC takes a **new snapshot per statement**, so a multi-statement read sees a moving world; SI takes one snapshot for the whole transaction and reports $1000. Same bug class breaks backups and analytical queries, which is why they run at RR/SI.

**Both permit lost update.** `SELECT counter` → app adds 1 → `UPDATE counter = 6`; two sessions do it concurrently and one increment vanishes. Fixes: an atomic write (`UPDATE ... SET n = n + 1`), an explicit `SELECT ... FOR UPDATE`, or compare-and-set on a version column. (Postgres RR does detect this particular one and aborts; MySQL RR does not.)

Interview framing: RC's guarantee is only "no dirty reads/writes" — it says nothing about a transaction seeing a *consistent* database.

## Q zh
给出读已提交允许但可重复读/快照隔离防止的具体异常，以及两者都允许的。

## A zh
**RC 允许读偏差（非重复读）。** 账户 A 和 B 各持有 $500。你的报告读取 A（$500），$100 的转账 A→B 提交，然后你的报告读取 B（$600） — 它报告 $1100，这笔钱从不存在。RC 对每个语句取**新快照**，所以多语句读见一个移动的世界；SI 为整个事务取一个快照并报告 $1000。同样的 bug 类破坏备份和分析查询，这就是为什么它们在 RR/SI 运行。

**两者都允许丢失更新。** `SELECT counter` → app 加 1 → `UPDATE counter = 6`；两个会话并发执行，一个增量消失。修复：原子写入（`UPDATE ... SET n = n + 1`），显式 `SELECT ... FOR UPDATE`，或版本列上的比较和设置。（Postgres RR 检测到这个特定的一个并中止；MySQL RR 不会。）

面试框架：RC 的保证仅是"没有脏读/写" — 它对事务看到**一致**的数据库无法说明。
