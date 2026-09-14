---
id: isolation-read-committed-only
node: txn.snapshot-isolation
type: qa
source: snowflake-docs
---
## Q
Snowflake 标准表支持哪几种事务隔离级别（isolation level）？在该级别下，一条语句能看到哪些数据？

## A
目前只支持 READ COMMITTED（读已提交）一种。一条语句只能看到在该语句开始之前已经提交的数据，永远看不到其他事务尚未提交的数据；读取基于语句开始时刻的已提交版本，因此读者不需要等待写者。
