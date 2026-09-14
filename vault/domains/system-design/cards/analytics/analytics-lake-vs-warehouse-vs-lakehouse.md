---
id: analytics-lake-vs-warehouse-vs-lakehouse
node: analytics.warehouse
type: qa
---
## Q
Warehouse vs data lake vs lakehouse — what does each own, and what gap does the lakehouse close?

## A
- **Warehouse** (Snowflake, BigQuery): the engine owns storage *and* format — great SQL performance, transactions, governance; but data is locked to one engine and non-SQL access (ML, Spark) is awkward.
- **Data lake**: raw files (Parquet) in object storage, any engine reads them — cheap and open, but no transactions, no schema enforcement, easy to rot into a "data swamp".
- **Lakehouse**: lake storage + an **open table format** (Iceberg/Delta) adding ACID commits, schema evolution, and time travel — so multiple engines share one governed copy.

The lakehouse closes the gap of choosing between *open/cheap* and *reliable/managed*.

## Q zh
Warehouse vs data lake vs lakehouse — 每个拥有什么，lakehouse 关闭什么间隙？

## A zh
- **Warehouse**（Snowflake、BigQuery）：引擎拥有存储*和*格式 — 很棒的 SQL 性能、transaction、governance；但数据锁定到一个引擎，非 SQL 访问（ML、Spark）很尴尬。
- **Data lake**：原始文件（Parquet）在对象存储，任何引擎读它们 — 便宜和开放，但没有 transaction、没有 schema 强制，容易腐烂成"data swamp"。
- **Lakehouse**：lake 存储 + **开放 table 格式**（Iceberg/Delta）添加 ACID 提交、schema 演化、时间旅行 — 所以多个引擎共享一个管理的副本。

Lakehouse 关闭*开放/便宜*和*可靠/托管*之间选择的间隙。
