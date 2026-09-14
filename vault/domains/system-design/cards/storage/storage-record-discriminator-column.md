---
id: storage-record-discriminator-column
node: storage.record-modeling
type: qa
---
## Q
You store several kinds of similar records — say invoices, credit notes, and refunds. Option A: one table with a `kind` discriminator column. Option B: one table per kind. What does each option make easy and each make painful?

## A
**Single table + discriminator** wins on *shared behavior*:
- Queries spanning kinds ("all financial events for account X, in time order") are one indexed scan — no UNIONs, one pagination cursor, one foreign key for other tables to reference.
- New kinds ship without DDL, and shared machinery (audit, archival, permissions) is written once.
- Pain: kind-specific columns go nullable-for-everyone, so the database can no longer enforce "refunds must have `original_invoice_id`" — per-kind constraints and validation migrate into application code (partial constraints/check-by-kind help but stay awkward). Every index and vacuum also spans all kinds, so one hot kind bloats costs for the rest.

**Table per kind** wins on *divergence*: exact NOT NULL/foreign-key constraints per kind, independent indexes and retention, no discriminator branching in code. Pain: cross-kind queries and references become UNIONs or a parallel "events" table you must keep in sync.

Heuristic: split when the kinds share little schema *and* are rarely queried together; discriminate when the shared timeline/reference is the primary access path.

## Q zh
你要存储几种相似的记录 — 比如发票、红字发票（credit note）、退款。方案 A：一张表加一个 `kind` 判别列（discriminator）。方案 B：每种记录一张表。两个方案各让什么变容易、各让什么变痛苦？

## A zh
**单表 + 判别列**赢在*共享行为*上：
- 跨类型的查询（"账户 X 的全部财务事件，按时间排序"）就是一次带索引的扫描 — 不需要 UNION，一个分页游标，其他表引用时只需一个外键。
- 新类型上线不需要 DDL，共享机制（审计、归档、权限）只写一次。
- 痛点：类型特有的列变成对所有人可空，数据库因此无法强制"退款必须有 `original_invoice_id`" — 按类型的约束和校验迁移进应用代码（partial constraint / 按 kind 的 check 有帮助但仍别扭）。每个索引和 vacuum 也横跨所有类型，一个热门类型会抬高其余类型的成本。

**每类型一张表**赢在*分化*上：每种类型有精确的 NOT NULL/外键约束、独立的索引和保留策略，代码里没有按判别列的分支。痛点：跨类型查询和引用变成 UNION，或者需要一张你必须保持同步的平行"事件"表。

启发式：当各类型几乎不共享 schema *且*很少被一起查询时拆表；当共享的时间线/引用是主要访问路径时用判别列。
