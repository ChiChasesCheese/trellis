---
id: isolation-sees-own-uncommitted-writes
node: txn.snapshot-isolation
type: qa
source: snowflake-docs
---
## Q
在一个尚未提交的事务里，先 `INSERT INTO t VALUES (1)`，再 `SELECT * FROM t`。这条 SELECT 能看到刚插入的行吗？其他会话呢？

## A
本事务内的 SELECT 能看到：READ COMMITTED（读已提交）下，一条语句会看到同一事务中先前语句所做的改动，即使这些改动尚未提交。其他会话看不到，因为对它们来说这是未提交数据，只有在该事务 COMMIT 之后开始的语句才能看到。
