---
id: at-before-statement-recover-bad-delete
node: continuity.at-before-statement-syntax
type: qa
source: snowflake-docs
---
## Q
有人执行了一条误删大量行的 DELETE，你拿到了它的查询 ID。应该用 `AT(STATEMENT => id)` 还是 `BEFORE(STATEMENT => id)` 来找回删除前的数据？为什么？

## A
用 `BEFORE(STATEMENT => id)`。BEFORE 表示「紧挨在该点之前」，返回的数据截止到但不包括这条语句所做的改动，正好是 DELETE 执行前的状态；AT 表示「恰好在该点」的状态。找回数据可以直接 `SELECT ... BEFORE(STATEMENT => id)`，或用 `CREATE TABLE ... CLONE ... BEFORE(STATEMENT => id)` 克隆出删除前的表。
