---
id: qas-find-candidates
node: pruning.query-acceleration-service
type: qa
source: snowflake-docs
---
## Q
在决定为哪个仓库开启查询加速服务（QAS）、设置多大扩展系数之前，用什么手段评估哪些查询会受益？

## A
两种途径：查询 ACCOUNT_USAGE 中的 `QUERY_ACCELERATION_ELIGIBLE` 视图，它为每条查询给出可被加速的执行时间，可按仓库汇总找出受益最大的仓库及其扩展系数上限分布；或者对某条已执行过的查询调用 `SYSTEM$ESTIMATE_QUERY_ACCELERATION`，若符合条件会返回不同扩展系数下的预估执行时间，不符合则在 `ineligibleReason` 中说明原因。
