---
id: storage-schema-on-read
node: storage.nosql
type: qa
---
## Q
"Schemaless" document stores still have a schema. Where does it live, and when is schema-on-read genuinely better than schema-on-write?

## A
It's **implicit in the reading code** (schema-on-read): the database enforces nothing, so every consumer must handle every historical shape ever written. Schema-on-write (relational DDL) enforces one shape at insert time.

Schema-on-read wins when:
- Records are **genuinely heterogeneous** (per-integration payloads, user-defined fields) — a fixed schema would be a sparse mess of nullable columns.
- Shape is dictated by **external systems** you don't control.
- Evolution: new fields just appear — no migration step; readers use defaults for old records.

The trade: relational `ALTER TABLE` is a one-time explicit migration (fast in Postgres — metadata-only for nullable adds); schema-on-read smears that migration across all reading code **forever**.

## Q zh
"无模式"文档存储仍有 schema。它住在哪里，什么时候 schema-on-read 真的比 schema-on-write 更好？

## A zh
它**隐含在读取代码中**（schema-on-read）：数据库强制不了什么，所以每个消费者必须处理每个历史形状曾经写的。Schema-on-write（关系 DDL）在插入时强制一个形状。

Schema-on-read 在以下情况胜出：
- 记录是**真正异质的**（每集成负载、用户定义字段）——固定 schema 会是可空列的稀疏混乱。
- 形状由**你无法控制的外部系统**指定。
- 演进：新字段就出现——无迁移步骤；读端对旧记录使用默认值。

权衡：关系 `ALTER TABLE` 是一次性显式迁移（在 Postgres 中快——可空添加的仅元数据）；schema-on-read 把那个迁移涂布在所有读代码中**永远**。
