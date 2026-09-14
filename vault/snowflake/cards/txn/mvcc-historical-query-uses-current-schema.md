---
id: mvcc-historical-query-uses-current-schema
node: txn.mvcc-immutable-partitions
type: qa
source: snowflake-docs
---
## Q
表 `orders` 昨天删除了一列 `coupon`。今天用 `SELECT * FROM orders AT(OFFSET => -86400*2)` 查询两天前的数据，结果里会有 `coupon` 列吗？

## A
不会。查询表或非物化视图的历史数据时，Snowflake 使用的是当前的表结构（schema）而不是历史结构；时间旅行（Time Travel）回溯的是数据版本，列定义按现在的表来解释。所以被删除的列在历史查询结果中也不会出现。
