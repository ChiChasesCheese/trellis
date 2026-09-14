---
id: isolation-statement-level-not-txn-level
node: txn.snapshot-isolation
type: qa
source: snowflake-docs
---
## Q
在一个多语句事务中，先后执行两次完全相同的 `SELECT COUNT(*) FROM orders`，中间另一个会话提交了一批 INSERT。两次结果会一样吗？为什么？

## A
可能不一样。在 READ COMMITTED（读已提交）隔离级别下，可见性是按语句（statement）而不是按事务确定的：每条语句看到的是它自己开始之前已提交的数据。如果另一事务在两条语句之间提交，第二条语句就会看到新行。需要整个事务内读到同一份快照的逻辑，不能依赖重复读取得到相同结果。
