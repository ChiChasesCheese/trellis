---
id: hi-c-sd-postgres-n29-sql-types
node: sd.deep-dives.postgres.notes
type: qa
step: 29
---
## Q
**PostgreSQL · SQL 的四类命令**｜摘要 · 追问

SQL 命令分哪几类？面试里需要多会写 SQL？

## A
- **DDL（数据定义）：** `CREATE TABLE`、`ALTER TABLE`、`DROP TABLE`，创建和修改结构。
- **DML（数据操作）：** `SELECT`、`INSERT`、`UPDATE`、`DELETE`，管理表里的数据。
- **DCL（数据控制）：** `GRANT`、`REVOKE`，管权限，如给只读用户授予 `SELECT`。
- **TCL（事务控制）：** `BEGIN`、`COMMIT`、`ROLLBACK`。
- **深度：** 系统设计面试很少让你写真正的 SQL，更多问"怎么高效查询这些数据""建什么索引"，考的是概念而不是语法；面向初级岗位时才可能让写基础查询。
