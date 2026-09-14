---
id: stream-advance-without-consuming
node: pipelines.stream-consumption-and-offset-advance
type: qa
source: snowflake-docs
---
## Q
流里积压了一大批不再需要的历史变更，想把偏移量直接跳到当前表版本而不处理这些数据。有哪两种做法？

## A
1) 用 `CREATE OR REPLACE STREAM` 重建流，新流的偏移量就是当前版本；2) 执行一条 INSERT 到临时表的语句，在其中查询该流但加上过滤掉全部数据的条件（如 `WHERE 0 = 1`）。第二种做法中，流在一个 DML 事务里被使用并提交，因此偏移量前移，但不会写入任何行。
