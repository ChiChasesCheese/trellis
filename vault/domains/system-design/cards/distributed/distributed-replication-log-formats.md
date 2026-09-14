---
id: distributed-replication-log-formats
node: distributed.replication.leader
type: qa
---
## Q
Statement-based vs WAL shipping vs logical (row-based) replication — what breaks or binds with each, and which do modern systems default to?

## A
- **Statement-based** (ship the SQL): breaks on nondeterminism — `NOW()`, `RAND()`, auto-increments, triggers, concurrent-execution order. Requires rewriting statements to be deterministic; mostly abandoned as a default.
- **WAL shipping** (ship physical block changes): exact but **couples replicas to the storage-engine version and layout** — leader and follower must run compatible versions, blocking zero-downtime rolling upgrades across versions.
- **Logical (row-based)** (ship row insert/update/delete records): decoupled from engine internals — enables cross-version replication, and is the basis of **CDC** to external systems (Debezium reading Postgres logical decoding / MySQL binlog `ROW` format).

Default answer: logical/row-based for flexibility; WAL shipping inside a single homogeneous cluster.

## Q zh
基于语句、WAL 传输、逻辑（行级）复制——各自在哪会出问题或被什么绑死？现代系统默认用哪种？

## A zh
- **基于语句**（传输 SQL 本身）：在非确定性面前会出问题——`NOW()`、`RAND()`、自增列、触发器、并发执行顺序。需要把语句改写成确定性的；基本已经被弃用为默认方案。
- **WAL 传输**（传输物理块级别的变更）：精确，但会**把副本和存储引擎的版本、布局死死绑在一起**——leader 和 follower 必须运行兼容的版本，这会阻碍跨版本的零停机滚动升级。
- **逻辑（行级）复制**（传输行的 insert/update/delete 记录）：和引擎内部实现解耦——使跨版本复制成为可能，也是对外部系统做 **CDC** 的基础（Debezium 读取 Postgres 的逻辑解码 / MySQL 的 binlog `ROW` 格式）。

默认答案：出于灵活性用逻辑/行级复制；在单一同构集群内部用 WAL 传输。
