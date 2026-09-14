---
id: mvcc-long-query-delays-failsafe-transition
node: txn.mvcc-immutable-partitions
type: qa
source: snowflake-docs
---
## Q
一条运行了几个小时、读取历史版本的时间旅行（Time Travel）查询，对账户里其他过期数据的清理有什么副作用？为什么会这样？

## A
它会推迟账户中数据和对象（表、模式、数据库）转入故障保护（Fail-safe）的过程，直到该查询结束。原因是旧的表版本仍被一个正在运行的查询所读取，在它读完之前不能把这些历史数据移出可访问的时间旅行存储。
