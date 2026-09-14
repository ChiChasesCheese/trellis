---
id: mvcc-dml-preserves-previous-version
node: txn.mvcc-immutable-partitions
type: qa
source: snowflake-docs
---
## Q
对 Snowflake 表执行 UPDATE 或 DELETE 后，被改掉的旧数据去哪了？这种做法让什么能力成为可能？

## A
Snowflake 不就地覆盖旧数据，而是在一个数据保留期（data retention period）内保留修改前的表数据版本，新写入产生新的表版本。正因为旧版本仍然存在，才可以用时间旅行（Time Travel）查询过去某个时间点的数据、基于过去的状态克隆表，或恢复被删除的对象；保留期结束后，历史数据转入故障保护（Fail-safe），这些操作就不再可行。
